import xml.etree.ElementTree as ET
tree = ET.parse('marth_rec2.xml')
root = tree.getroot()
for elem in root.iter():
    if elem.tag.find("/sitemap/") > 0:
         if elem.tag.find("loc") > 0:
            txt = "\'" + str(elem.text.lstrip()) + "\'"
            print("Saving to:", txt )


#for elem in root.iter():
#    try:
#       print(elem.text)
#    except:
#       print("unicode error")

# Saving to: 'www.marthastewart.com/index.html'

