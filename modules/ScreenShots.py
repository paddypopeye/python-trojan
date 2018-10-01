import win32gui
import win32ui
import win32con
import win32api

#get handle to main Desktop window
desktophand = win32gui.GetDesktopWindow()
#Determine Window size
width = win32api.GetSyetemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSyetemMetrics(win32con.SM_CYVIRTUALSCREEN)
top = win32api.GetSyetemMetrics(win32con.SM_XVIRTUALSCREEN)
left = win32api.GetSyetemMetrics(win32con.SM_YVIRTUALSCREEN)

#Desktop Context
desktop_context = win32gui.GetWindowDC(desktophand)
img_context = win32ui.CreateDCFromHandle(desktop_context)
#Memory based device context 
memory_context = img_context.CreateCompatibleDC()
#Bitmap object
screenshot  = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_context,width,height)
memory_context.BitBit((0,0),(width,height),img_context, (left,top),win32con.SRCCOPY)
#Save Bitmap 
screenshot.SaveBitmapFile(memory_context, "home/eugene/screenshots")
#Free objects
memory_context.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())