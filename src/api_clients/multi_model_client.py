"""
Multi-Model API Client with Rate Limiting and Cost Tracking
Supports Claude, GPT-5, and Gemini with intelligent routing
"""
import time
import asyncio
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import anthropic
import openai
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import threading
from collections import deque


class ModelProvider(Enum):
    """Supported model providers"""
    CLAUDE = "claude"
    OPENAI = "openai"
    GEMINI = "gemini"


@dataclass
class APICall:
    """Track individual API call"""
    timestamp: datetime
    provider: ModelProvider
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency: float
    success: bool
    error: Optional[str] = None


class RateLimiter:
    """Thread-safe rate limiter using token bucket algorithm"""
    
    def __init__(self, requests_per_minute: int):
        self.rpm = requests_per_minute
        self.tokens = requests_per_minute
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def acquire(self, blocking: bool = True) -> bool:
        """Acquire permission to make a request"""
        with self.lock:
            now = time.time()
            # Refill tokens based on time elapsed
            elapsed = now - self.last_update
            self.tokens = min(self.rpm, self.tokens + elapsed * (self.rpm / 60.0))
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            elif blocking:
                # Wait until we have tokens
                sleep_time = (1 - self.tokens) * (60.0 / self.rpm)
                time.sleep(sleep_time)
                self.tokens = 0
                self.last_update = time.time()
                return True
            else:
                return False


class CostTracker:
    """Track API costs across all providers"""
    
    def __init__(self, pricing: Dict[str, Dict[str, float]]):
        self.pricing = pricing
        self.call_history: List[APICall] = []
        self.lock = threading.Lock()
        
        # Running totals
        self.total_cost = 0.0
        self.costs_by_provider = {provider: 0.0 for provider in ModelProvider}
        self.costs_by_model = {}
    
    def track_call(self, api_call: APICall):
        """Track an API call"""
        with self.lock:
            self.call_history.append(api_call)
            self.total_cost += api_call.cost
            self.costs_by_provider[api_call.provider] += api_call.cost
            
            if api_call.model not in self.costs_by_model:
                self.costs_by_model[api_call.model] = 0.0
            self.costs_by_model[api_call.model] += api_call.cost
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for given token usage"""
        if model not in self.pricing:
            return 0.0
        
        pricing = self.pricing[model]
        cost = (input_tokens * pricing['input'] / 1_000_000 +
                output_tokens * pricing['output'] / 1_000_000)
        return cost
    
    def get_summary(self) -> Dict:
        """Get cost tracking summary"""
        with self.lock:
            total_calls = len(self.call_history)
            successful_calls = sum(1 for call in self.call_history if call.success)
            failed_calls = total_calls - successful_calls
            
            return {
                'total_cost': self.total_cost,
                'total_calls': total_calls,
                'successful_calls': successful_calls,
                'failed_calls': failed_calls,
                'costs_by_provider': {p.value: c for p, c in self.costs_by_provider.items()},
                'costs_by_model': self.costs_by_model,
                'avg_cost_per_call': self.total_cost / total_calls if total_calls > 0 else 0
            }
    
    def print_summary(self):
        """Print formatted cost summary"""
        summary = self.get_summary()
        
        print("\n" + "="*80)
        print("API COST TRACKING SUMMARY")
        print("="*80)
        print(f"\nTotal Cost: ${summary['total_cost']:.2f}")
        print(f"Total Calls: {summary['total_calls']} ({summary['successful_calls']} successful, {summary['failed_calls']} failed)")
        print(f"Avg Cost/Call: ${summary['avg_cost_per_call']:.4f}")
        
        print(f"\nCosts by Provider:")
        for provider, cost in summary['costs_by_provider'].items():
            print(f"  {provider.capitalize()}: ${cost:.2f}")
        
        print(f"\nCosts by Model:")
        for model, cost in sorted(summary['costs_by_model'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {model}: ${cost:.2f}")
        
        print("="*80)


class MultiModelClient:
    """
    Unified client for Claude, GPT-5, and Gemini
    Features: rate limiting, cost tracking, automatic retries
    """
    
    def __init__(self, config):
        """Initialize with configuration"""
        self.config = config
        
        # Initialize API clients
        self.claude = anthropic.Anthropic(api_key=config.api.anthropic_api_key)
        self.openai_client = openai.OpenAI(api_key=config.api.openai_api_key)
        genai.configure(api_key=config.api.gemini_api_key)
        self.gemini = genai.GenerativeModel(config.api.gemini_model)
        
        # Initialize rate limiters
        self.rate_limiters = {
            ModelProvider.CLAUDE: RateLimiter(config.api.claude_rpm),
            ModelProvider.OPENAI: RateLimiter(config.api.openai_rpm),
            ModelProvider.GEMINI: RateLimiter(config.api.gemini_rpm),
        }
        
        # Initialize cost tracker
        self.cost_tracker = CostTracker(config.api.pricing)
        
        print("✅ Multi-Model API Client initialized")
        print(f"   Claude: {config.api.claude_model}")
        print(f"   OpenAI: {config.api.gpt_model}")
        print(f"   Gemini: {config.api.gemini_model}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_claude(self, 
                       prompt: str,
                       max_tokens: Optional[int] = None,
                       temperature: Optional[float] = None) -> Dict:
        """Generate content using Claude"""
        
        provider = ModelProvider.CLAUDE
        model = self.config.api.claude_model
        
        # Wait for rate limit
        self.rate_limiters[provider].acquire()
        
        start_time = time.time()
        
        try:
            response = self.claude.messages.create(
                model=model,
                max_tokens=max_tokens or self.config.api.claude_max_tokens,
                temperature=temperature or self.config.api.claude_temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            latency = time.time() - start_time
            
            # Extract content
            content = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            
            # Calculate cost
            cost = self.cost_tracker.calculate_cost(model, input_tokens, output_tokens)
            
            # Track call
            api_call = APICall(
                timestamp=datetime.now(),
                provider=provider,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                latency=latency,
                success=True
            )
            self.cost_tracker.track_call(api_call)
            
            return {
                'content': content,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': cost,
                'latency': latency,
                'model': model
            }
            
        except Exception as e:
            latency = time.time() - start_time
            api_call = APICall(
                timestamp=datetime.now(),
                provider=provider,
                model=model,
                input_tokens=0,
                output_tokens=0,
                cost=0.0,
                latency=latency,
                success=False,
                error=str(e)
            )
            self.cost_tracker.track_call(api_call)
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_gpt5(self,
                     prompt: str,
                     max_tokens: Optional[int] = None,
                     temperature: Optional[float] = None) -> Dict:
        """Generate content using GPT-5"""
        
        provider = ModelProvider.OPENAI
        model = self.config.api.gpt_model
        
        # Wait for rate limit
        self.rate_limiters[provider].acquire()
        
        start_time = time.time()
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                max_tokens=max_tokens or self.config.api.gpt_max_tokens,
                temperature=temperature or self.config.api.gpt_temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            latency = time.time() - start_time
            
            # Extract content
            content = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            # Calculate cost
            cost = self.cost_tracker.calculate_cost(model, input_tokens, output_tokens)
            
            # Track call
            api_call = APICall(
                timestamp=datetime.now(),
                provider=provider,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                latency=latency,
                success=True
            )
            self.cost_tracker.track_call(api_call)
            
            return {
                'content': content,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': cost,
                'latency': latency,
                'model': model
            }
            
        except Exception as e:
            latency = time.time() - start_time
            api_call = APICall(
                timestamp=datetime.now(),
                provider=provider,
                model=model,
                input_tokens=0,
                output_tokens=0,
                cost=0.0,
                latency=latency,
                success=False,
                error=str(e)
            )
            self.cost_tracker.track_call(api_call)
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_gemini(self,
                       prompt: str,
                       max_tokens: Optional[int] = None,
                       temperature: Optional[float] = None) -> Dict:
        """Generate content using Gemini"""
        
        provider = ModelProvider.GEMINI
        model = self.config.api.gemini_model
        
        # Wait for rate limit
        self.rate_limiters[provider].acquire()
        
        start_time = time.time()
        
        try:
            response = self.gemini.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens or self.config.api.gemini_max_tokens,
                    temperature=temperature or self.config.api.gemini_temperature
                )
            )
            
            latency = time.time() - start_time
            
            # Extract content
            content = response.text
            
            # Gemini doesn't always return token counts reliably
            # Estimate tokens (rough approximation)
            input_tokens = int(len(prompt.split()) * 1.3)
            output_tokens = int(len(content.split()) * 1.3)
            
            # Calculate cost
            cost = self.cost_tracker.calculate_cost("gemini-3-flash", input_tokens, output_tokens)
            
            # Track call
            api_call = APICall(
                timestamp=datetime.now(),
                provider=provider,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                latency=latency,
                success=True
            )
            self.cost_tracker.track_call(api_call)
            
            return {
                'content': content,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': cost,
                'latency': latency,
                'model': model
            }
            
        except Exception as e:
            latency = time.time() - start_time
            api_call = APICall(
                timestamp=datetime.now(),
                provider=provider,
                model=model,
                input_tokens=0,
                output_tokens=0,
                cost=0.0,
                latency=latency,
                success=False,
                error=str(e)
            )
            self.cost_tracker.track_call(api_call)
            raise
    
    def generate(self,
                prompt: str,
                provider: Literal["claude", "gpt5", "gemini"],
                max_tokens: Optional[int] = None,
                temperature: Optional[float] = None) -> Dict:
        """Generate content using specified provider"""
        
        if provider == "claude":
            return self.generate_claude(prompt, max_tokens, temperature)
        elif provider == "gpt5":
            return self.generate_gpt5(prompt, max_tokens, temperature)
        elif provider == "gemini":
            return self.generate_gemini(prompt, max_tokens, temperature)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def get_cost_summary(self) -> Dict:
        """Get cost tracking summary"""
        return self.cost_tracker.get_summary()
    
    def print_cost_summary(self):
        """Print cost tracking summary"""
        self.cost_tracker.print_summary()


if __name__ == "__main__":
    # Test the multi-model client
    from config import Config
    
    config = Config()
    client = MultiModelClient(config)
    
    # Test each provider
    test_prompt = "Write a brief explanation of photosynthesis for Grade 10 students."
    
    print("\n🧪 Testing Multi-Model API Client")
    print("="*80)
    
    try:
        print("\n1. Testing Gemini...")
        result = client.generate_gemini(test_prompt)
        print(f"   Cost: ${result['cost']:.4f}, Latency: {result['latency']:.2f}s")
        print(f"   Content preview: {result['content'][:100]}...")
        
        print("\n2. Testing GPT-5...")
        result = client.generate_gpt5(test_prompt)
        print(f"   Cost: ${result['cost']:.4f}, Latency: {result['latency']:.2f}s")
        print(f"   Content preview: {result['content'][:100]}...")
        
        print("\n3. Testing Claude...")
        result = client.generate_claude(test_prompt)
        print(f"   Cost: ${result['cost']:.4f}, Latency: {result['latency']:.2f}s")
        print(f"   Content preview: {result['content'][:100]}...")
        
        # Print cost summary
        client.print_cost_summary()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
