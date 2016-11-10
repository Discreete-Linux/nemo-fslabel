""" A nemo extension which allows renaming of volumes """
# Encoding: UTF-8
import gettext
from gi.repository import Gtk, Nemo, GObject
import subprocess
from multiprocessing import Process

class VolumeRenameExtension(GObject.GObject, Nemo.MenuProvider):
    """ Allows renaming of volumes from the nemo desktop """
    def __init__(self):
        """ Init the extionsion, currently does nothing. """
        print "Initializing nemo-volume-rename extension"

    def menu_activate_cb(self, menu, myfile):
        """ Handle menu activation, i.e. actual renaming """
        mountpoint = myfile.get_mount().get_root().get_path()
        label = Gtk.Label(gettext.dgettext('nemo-fslabel', "Enter new label:").decode('utf-8'))
        dlg = Gtk.Dialog(title=gettext.dgettext('nemo-fslabel', "Rename volume").decode('utf-8'), 
                        buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
                        Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dlg.set_position(Gtk.WindowPosition.CENTER)
        dlg.vbox.pack_start(label, True, True, 0)
        label.show()
        entry = Gtk.Entry()
        entry.set_max_length(16)
        entry.set_text(myfile.get_name().rpartition('.')[0])
        dlg.vbox.pack_start(entry, True, True, 0)
        entry.show()
        response = dlg.run()
        newlabel = entry.get_text().decode("ASCII", "ignore").encode("ASCII")
        dlg.destroy()
        while Gtk.events_pending():
            Gtk.main_iteration()
        if response != Gtk.ResponseType.OK:
            return
        Process(target=subprocess.call, args =(("/usr/bin/fslabel", "-m", mountpoint, newlabel), )).start()
        return
        
    def get_file_items(self, window, files):
        """ Tell nemo whether and when to show the menu """
        if len(files) != 1:
            return
        myfile = files[0]
        if not (
            ( ( myfile.get_uri_scheme() == 'x-nemo-desktop' ) and 
            ( myfile.get_mime_type() == 'application/x-nemo-link' ) ) or 
            ( myfile.get_uri_scheme() == 'computer') ):
            return        
        item = Nemo.MenuItem(name='Nemo::volume_rename',
                                 label=gettext.dgettext('nemo-fslabel', 'Rename volume').decode('utf-8'),
                                 tip=gettext.dgettext('nemo-fslabel', 'Renames the current volume').decode('utf-8'))
        item.connect('activate', self.menu_activate_cb, myfile)
        return [item]
