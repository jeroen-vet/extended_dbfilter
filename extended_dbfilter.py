from odoo.http import request, db_filter
from odoo import config
import re
try:
    from publicsuffix import PublicSuffixList
except ImportError:
    raise ImportError("The 'publicsuffix' library is required. Install it with: pip install publicsuffix")

def extended_db_filter(dbs, host=None):
    """Custom db_filter function to add %s placeholder for Second-Level Domain (SLD).

    Overrides Odoo's db_filter function in odoo.http to introduce a %s placeholder
    that extracts the SLD from the hostname (e.g., 'domain' from 'x.domain.com' or
    'domain.co.uk') using the publicsuffix library. Retains default %h (hostname
    without www.) and %d (first part of hostname) behaviors. Prioritizes matching
    in order: %d, %s, %h, then full regex. Returns a single database name to avoid
    the database selector screen, unless the regex yields multiple matches.

    Usage:
    - Set dbfilter in odoo.conf (e.g., dbfilter = ^(%s|fallback_db)$).
    - Name databases after the SLD or other patterns as needed.
    - Requires the 'publicsuffix' Python library.

    Args:
        dbs (Iterable[str]): List of available database names to filter.
        host (str, optional): Hostname from HTTP_HOST. Defaults to request.httprequest.environ['HTTP_HOST'].

    Returns:
        list: A single database name in a list, prioritizing %d, %s, %h, then regex matches.
    """
    if config['dbfilter']:
        # Extract hostname
        if host is None:
            host = request.httprequest.environ.get('HTTP_HOST', '')
        host = host.partition(':')[0]
        if host.startswith('www.'):
            host = host[4:]  # e.g., x.domain.com

        # Default %d: first part of hostname
        domain = host.partition('.')[0]  # e.g., x for x.domain.com, domain for domain.com

        # New %s: Second-Level Domain using publicsuffix
        psl = PublicSuffixList()
        base_domain = psl.get_public_suffix(host)  # e.g., domain.com, otherdomain.co.uk
        sld = base_domain.split('.')[0] if base_domain else host  # e.g., domain, otherdomain

        # Priority 1: Check for %d occurrence and exact match
        if '%d' in config['dbfilter'] and domain in dbs:
            return [domain]

        # Priority 2: Check for %s occurrence and exact match
        if '%s' in config['dbfilter'] and sld in dbs:
            return [sld]

        # Priority 3: Check for %h occurrence and exact match
        if '%h' in config['dbfilter'] and host in dbs:
            return [host]

        # Priority 4: Apply full regex with substitutions
        dbfilter_re = re.compile(
            config["dbfilter"].replace("%h", re.escape(host))
                             .replace("%d", re.escape(domain))
                             .replace("%s", re.escape(sld))
        )
        return [db for db in dbs if dbfilter_re.match(db)] or []

    if config['db_name']:
        # Handle --database option
        exposed_dbs = {db.strip() for db in config['db_name'].split(',')}
        matches = sorted(exposed_dbs.intersection(dbs))
        return [matches[0]] if matches else []

    return [dbs[0]] if dbs else []

# Monkey-patch the original db_filter function
from odoo import http
http.db_filter = extended_db_filter