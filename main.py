##  Required imports
import matplotlib; matplotlib.use('Agg')
import sdesk
import os
import numpy as np
from matplotlib import pyplot as plt
import hyperspy.api as hs
hs.preferences.GUIs.enable_traitsui_gui = False
hs.preferences.GUIs.enable_ipywidgets = False
hs.preferences.GUIs.warn_if_guis_are_missing = False
##


# Define your method main()
def main():
    process = sdesk.Process()

    # LOAD INPUT FILES OR SAMPLES
    input_file = process.input_files[0] 
    file_name, file_extension = os.path.splitext(input_file.properties['name']) 
    if file_extension.lower() not in ['.msa']:
        """ STOP AND DO NOTHING """
        return 0
    
    # LOAD PARAMETERS FROM USER INPUT FORM
    input_form = process.arguments 
    
    # PROCESS INPUT FILE AND EXTRACT DATA
    s = hs.load(input_file.path)
    x_axis = s.axes_manager[-1]
    last_x = x_axis.offset + x_axis.scale*x_axis.size
    x_np = np.linspace(x_axis.offset, last_x, x_axis.size )
    xy_np = np.array([x_np,s.data]).transpose()
    
    # CREATE THUMBNAIL IMAGE
    sdesk_thumbnail = process.create_output_file('_thumbnail_picture.png')
    s.plot(); fig = plt.gcf() 
    fig.savefig(sdesk_thumbnail.path)

    # UPDATE CUSTOM PROPERTIES OF INPUT FILE
    input_file.custom_properties.update(s.original_metadata.as_dictionary())
    input_file.save_custom_properties()

    # CREATE PARSED OUTPUT FILES
    out_file = { 'name':f"{file_name.split('.')[0]}_exported.txt",
                 'columns': ["energy loss","Electrons"],
                 'data': xy_np,
                 'header': sdesk.json_to_text(input_file.custom_properties)
              }
    
    sdesk_output_file = process.create_output_file(out_file['name'])
    sdesk.write_tsv_file(sdesk_output_file.path, out_file['columns'], out_file['data'],  out_file['header'])



# Call method main()
main()