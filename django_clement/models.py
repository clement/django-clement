from django.db.models import Manager
from django.db.models.query import QuerySet


class EagerLoadingQuerySet(QuerySet):
    def select_many_related(self, field, **kwargs):
        if not hasattr(self, 'eager_loads'):
            self.eager_loads = []

        d = dict()
        d.update(kwargs)
        d['field'] = field
        self.eager_loads.append(d)

        return self

    def _clone(self, *args, **kwargs):
        c = super(EagerLoadingQuerySet, self)._clone(*args, **kwargs)
        if hasattr(self, 'eager_loads'):
            c.eager_loads = self.eager_loads
        return c

    def iterator(self):
        _iter = super(EagerLoadingQuerySet, self).iterator()
        if not hasattr(self, 'eager_loads'):
            return _iter

        rows = {}
        original = []
        for row in _iter:
            rows[row.pk] = row
            original.append(row)

        for eager_load in self.eager_loads:
            related = self.model._meta.get_field_by_name(eager_load['field'])[0]
            qs = eager_load.get('queryset', related.model._default_manager.get_query_set())
            qs = qs.filter(**{'%s__in' % related.field.name : rows.keys()})

            loaded = dict([(pk, []) for pk in rows])
            for row in qs:
                loaded[getattr(row, related.field.attname)].append(row)

            for (pk, relateds) in loaded.items():
                setattr(rows[pk], eager_load.get('field_name', '%s_cache' % eager_load['field']), relateds)

        return iter(original)


class EagerLoadingManager(Manager):
    def get_query_set(self):
        qs = super(EagerLoadingManager, self).get_query_set()
        qs.__class__ = EagerLoadingQuerySet
        return qs

    def select_many_related(self, *args, **kwargs):
        return self.get_query_set().select_many_related(*args, **kwargs)


def cache_m2m(name, cache_name=None):
    if not cache_name:
        cache_name = '_'+name

    def fget(self):
        if not hasattr(self, cache_name):
            setattr(self, cache_name, getattr(self, name).all())
        return getattr(self, cache_name)
    def fset(self, value):
        setattr(self, cache_name, value)
    return property(fget, fset)
