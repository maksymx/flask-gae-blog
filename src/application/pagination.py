from math import ceil
from google.appengine.ext import ndb


class Pagination(object):
    def __init__(self, page, per_page, qry):
        self._page = page
        self._per_page = per_page
        self._qit = qry.iter(offset=(page - 1) * per_page, limit=per_page)
        self._pages = qry.count_async()

    @property
    def pages(self):
        total_count = self._pages.get_result()
        return int(ceil(total_count / float(self._per_page)))

    @property
    def has_prev(self):
        return self._page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    @ndb.tasklet
    def items(self):
        results = []
        while (yield self._qit.has_next_async()):
            entity = self._qit.next()
            results.append(entity)

        raise ndb.Return(results)

    @property
    def page(self):
        return self._page

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or (self.page - left_current - 1 < num < self.page + right_current) or \
                            num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num