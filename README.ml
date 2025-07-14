# Extebded DB Filter Module with SLD Placeholder

## Overview

This Odoo module extends the database selection logic by overriding the `db_filter` function in `odoo.http` to introduce a `%s` placeholder that extracts the **Second-Level Domain (SLD)** from the request hostname (e.g., `domain` from `x.domain.com` or `domain.co.uk`). It retains Odoo’s default `%h` (hostname without `www.`) and `%d` (first part of hostname) behaviors. The logic is changed so that if any of the selectors %d,%s or %h in that order have a match that match is returned as a single database. Only if none matches the regular expression is applied.


### Purpose
- Allows a complex multi tenant database with multiple database and multiple website. Ideal for developers and hosting. So you could have a default database that has multiple websites for different domains or subdomains, databases for different domains and databases for different subdomains. A domain database could also have multiple websites as long as these websites  have urls with a subdomain for that domain and there is no database matching those subdomains.
- Routes requests for a hostname (e.g., `domain.com`, `x.domain.com`, `domain.co.uk`) to a database named after the SLD (e.g., `domain`).
- Uses the `publicsuffix` library for accurate SLD extraction, supporting simple TLDs (`.com`, `.nl`, `.biz`) and complex TLDs (`.co.uk`, `.com.cn`).
- Designed for Odoo 17 (compatible with Odoo 18, as `dbfilter` logic is unchanged).

### Assumptions
- Databases are named after the subdomains or the SLD (e.g., `domain` for `x.domain.com`, `otherdomain` for `site1.otherdomain.com`) or the host or some other name matching the regular expression (for example a default database).
- The `publicsuffix` Python library is installed.

