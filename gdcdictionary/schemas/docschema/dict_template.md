{# Jinja template for GDC dictionary render in markdown #}
{# input vars : obj - the dictionary json object #}
{#              gloss - dict mapping term names to term objs #}

# _Entry_: {{ obj.title }} (category: _{{obj.category}}_) #


{% if gloss.get_definition(obj.id) is defined %}
{{ gloss.get_definition(obj.id) }}
{% elif obj.description is defined and obj.description != 'TBD'%}
{{ obj.description }}
{% else %}
_Coming Soon_
{% endif %}
{% if gloss.get_cde_info(obj.id) is defined %}
  {% set cdeinfo = gloss.get_cde_info(obj.id) %}
  {% if cdeinfo.collection_url %}
_CDE_: [{{cdeinfo.cde_id}}]({{cdeinfo.collection_url}})
  {% else %}
_CDE_: {{cdeinfo.cde_id}}
  {% endif %}
{% endif %}

{% if obj.properties is defined %}
## Properties ##
| Property | Acceptable Type or Values |
| --- | --- |
{% for prop, propv in obj.properties.iteritems() %}
  {% if propv.type is defined %}
| [{{prop}}](#{{prop}}) | _{{propv.type}}_ |
  {% elif propv.enum is defined %}
| [{{prop}}](#prop) | "{{ propv.enum|join('", "') }}" |
  {% endif %}
{% endfor %}
{% endif %}

## Terms ##
| Term | Definition | Collection | CDE |
| --- | --- | --- | --- |
{% for prop in obj.properties.keys() %}
|<a name="#{{prop}}"></a> {{prop}} | {{gloss.get_definition(prop)}} |
{{gloss.get_cde_info(prop).collection_name}} |
 [{{gloss.get_cde_info(prop).cde_id}}]({{gloss.get_cde_info(prop).collection_url}})|
{% endfor %}


