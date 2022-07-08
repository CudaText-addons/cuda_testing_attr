from cudatext import *
from itertools import product
import random
import time

class Command:
    def run(self):
        h = dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={'border': DBORDER_SIZE,'w': 1000,'h': 600, 'keypreview': True, 'on_key_press': self.form_key_press})
        n = dlg_proc(h, DLG_CTL_ADD, 'editor')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={ 'name': 'memo','a_r': ('', ']'), 'a_b': ('', ']'), 'font_size': 11 })
        self.h_dlg = h

        self.memo = Editor(dlg_proc(h, DLG_CTL_HANDLE, index=n))

        self.memo.set_text_all(('F'*70+'\n')*25)
        self.memo.set_prop(PROP_RO, True)

        #self.memo.attr(MARKERS_DELETE_BY_POS, x=0, y=0)

        dlg_proc(h, DLG_SHOW_NONMODAL)

    def form_key_press(self, id_dlg, id_ctl, data='', info=''):
        start = time.time()
        markers_added = 0

        print('start test',chr(id_ctl))

        if id_ctl == ord('1'):
            self.memo.attr(MARKERS_SET_DUPS, tag=1) # test 1
        if id_ctl == ord('2'):
            self.memo.attr(MARKERS_SET_DUPS, tag=0) # test 2


        count = 10
        while count > 0:
            markers_added = 0
            for x, y in product(range(70), range(25)):
                self.memo.attr(MARKERS_ADD, x=x, y=y, len=1, color_font=random.randint(0,255), color_bg=random.randint(0,255))
                markers_added += 1
            count -= 1

            #we can repaint memo every iteration here, but...
            #self.memo.action(EDACTION_UPDATE) # not repainting markers it seems.
            #app_idle() # repaints, but if I hold key it causes recursion into "form_key_press"?? how to avoid it?

        # print test results
        end = time.time()
        t = (end-start)*1000
        marker_count = len(self.memo.attr(MARKERS_GET))
        print('end. time={:.0f} ms, trash markers={}'.format(t, marker_count-markers_added))

        # update caption
        dlg_proc(self.h_dlg, DLG_PROP_SET, prop={
            'cap': '{} markers total, time={:.0f}'.format( marker_count, t )
        })
