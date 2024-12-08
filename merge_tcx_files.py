import re

def merge_tcx_files(tcx_paths, output_path):

    n_paths = len(tcx_paths)

    if n_paths == 0:
        return 'No paths provided'
    
     # Read the content of the TCX file
    with open(tcx_paths[0], 'r', encoding='utf-8') as file:
        content = file.read()

    if n_paths == 1:        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return 'File written to ' + output_path
    
    pre_lap_pattern = r'^.*?(<Lap)'
    after_lap_pattern = r'(.*</Lap>).*'
    merged_content = re.sub(after_lap_pattern, r'\1', content, flags=re.DOTALL)

    for n in range(1,n_paths):
        with open(tcx_paths[n], 'r', encoding='utf-8') as file:
            new_content = file.read()
        
        new_content = re.sub(pre_lap_pattern, r'\1', new_content, flags=re.DOTALL)

        if n < n_paths-1:
            new_content = re.sub(after_lap_pattern, r'\1', new_content, flags=re.DOTALL)

        merged_content = merged_content + new_content

    with open(output_path, 'w', encoding='utf-8') as file:
            file.write(merged_content)
    
    return 'File written to ' + output_path

#merge_tcx_files(['Lunch_Ride.tcx','Lunch_Ride.tcx','Lunch_Ride.tcx'],'boo.tcx')