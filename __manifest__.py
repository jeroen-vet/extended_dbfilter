{
    'name': 'Extended DB Filter with SLD Placeholder',
    'version': '1.0',
    'depends': ['web'],
    'installable': False,
    'auto_install': False,
    'external_dependencies': {
        'python': ['publicsuffix'],
    },
    'summary': 'Extends Odoo database filter with an %s placeholder for Second-Level Domains (SLD) and also returns only one database',
    'description': """
        This system wide module overrides Odoo's db_filter function in odoo.http to introduce a %s
        placeholder that extracts the Second-Level Domain (SLD) from the request hostname
        (e.g., 'domain' from 'x.domain.com' or 'domain.co.uk'). It retains default %h
        (hostname without www.) and %d (first part of hostname) behaviors, selecting
        databases named after the SLD. 
        If any selectors are matched, it also returns only one database to avoid users being confronted with the database selector.
        Only if there are no direct matches the regular expression is applied.

        Usage:
        - Set dbfilter = ^(%d|%s|%h|my_default_database)$ in odoo.conf.
        - Name databases after the SLD (e.g., 'domain', 'otherdomain') to be selectable.
        - Requires the 'publicsuffix' Python library:
            pip install publicsuffix
    """,
}