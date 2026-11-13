"""Workspace curation after matching; no production matcher changes."""


def exclusion_reason(policy, module, title, independent=False):
    if independent:
        return 'independent assessment'
    if any(term.lower() in title.lower() for term in policy.get('excluded_title_phrases', [])):
        return 'out-of-scope title'
    allowed = policy.get('module_allowed_titles', {})
    if module in allowed and title not in allowed[module]:
        return 'no independently vetted local match for this module; use supplied materials'
    return None
