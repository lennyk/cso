from django import template
from django.conf import settings

register = template.Library()

PIWIK_TRACKING_CODE = """
<script type="text/javascript">
  var _paq = _paq || [];
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u=(("https:" == document.location.protocol) ? "https" : "http") + "://%(url)s/";
    _paq.push(['setTrackerUrl', u+'piwik.php']);
    _paq.push(['setSiteId', %(siteid)s]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0]; g.type='text/javascript';
    g.defer=true; g.async=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img src="http://%(url)s/piwik.php?idsite=%(siteid)s" style="border:0;" alt="" /></p></noscript>
"""


@register.simple_tag
def piwik_javascript():
    if hasattr(settings, 'PIWIK_SITE_ID') and hasattr(settings, 'PIWIK_DOMAIN_PATH'):
        return PIWIK_TRACKING_CODE % {
            'url': settings.PIWIK_DOMAIN_PATH,
            'siteid': settings.PIWIK_SITE_ID,
        }
    return ''
