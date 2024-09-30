import os 
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--directory", help = 'name of parcellation scheme')
    parser.add_argument('-i', "--subid", help = 'subject BIDS id')
    parser.add_argument('-s', "--ses", help = 'session')
    args = parser.parse_args()

    # get all the file paths for the directory ''sub-s002_ses-01'
    # directory = 'ses-2'
    def get_file_paths(directory):
        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths

    def rename_files(directory, sub_id, file_path_num=2, session=None):
        file_paths = get_file_paths(directory)
        print(directory)
        print(f'is session none: {session is None}')
        print(file_paths)

        # for all files in the directory

        # create new directory called sub-<sub_id>
        os.mkdir(f'sub-{sub_id}')
        # check if a file exists    
        os.mkdir(f'misc_sub-{sub_id}')

        if session is None: 
            # make subdirectories for anat, fmap, and func in sub-<sub_id>
            os.mkdir(os.path.join(f'sub-{sub_id}', 'anat'))
            os.mkdir(os.path.join(f'sub-{sub_id}', 'fmap'))
            os.mkdir(os.path.join(f'sub-{sub_id}', 'func'))
        else: 
            os.mkdir(os.path.join(f'sub-{sub_id}', f'ses-{session}'))
            os.mkdir(os.path.join(f'sub-{sub_id}', f'ses-{session}','anat'))
            os.mkdir(os.path.join(f'sub-{sub_id}', f'ses-{session}','fmap'))
            os.mkdir(os.path.join(f'sub-{sub_id}',f'ses-{session}', 'func'))
            os.mkdir(os.path.join(f'misc_sub-{sub_id}', f'ses-{session}'))
            os.mkdir(os.path.join(f'misc_sub-{sub_id}', f'ses-{session}','anat'))
            os.mkdir(os.path.join(f'misc_sub-{sub_id}', f'ses-{session}','fmap'))
            os.mkdir(os.path.join(f'misc_sub-{sub_id}',f'ses-{session}', 'func'))

        for filepath in file_paths:
            # get the subdirectory
            subdirectory = filepath.split('/')[file_path_num-1]
            if subdirectory == '.DS_Store' or subdirectory == 'bids_heuristic.py':
                continue

            filename = filepath.split('/')[file_path_num]

            # rename the file
            if 'sidecars' in subdirectory:
                sidecar_type = "_".join(filepath.split('/')[file_path_num].split('_')[2:])
                
                if session is None:
                    new_filename = f'sub-{sub_id}_{sidecar_type}'
                else:
                    new_filename = f'sub-{sub_id}_ses-{session}_{sidecar_type}'
                
                if 'task' in new_filename:
                    new_subdirectory = 'func'
                else:
                    new_subdirectory = 'fmap'
                    
                print('new sidecars folder name:', new_filename)
                bids_name = f'sub-{sub_id}_{new_filename}'
            elif 'fmap-fieldmap' in subdirectory:
                new_subdirectory = 'fmap'
                if 'fieldmap.nii.gz' in filename:
                    if session is None:
                        bids_name = f'sub-{sub_id}_fieldmap.nii.gz'
                    else:
                        bids_name = f'sub-{sub_id}_ses-{session}_fieldmap.nii.gz'
                elif '_1.nii.gz' in filename:
                    if session is None:
                        bids_name = f'sub-{sub_id}_magnitude.nii.gz'
                    else:
                        bids_name = f'sub-{sub_id}_ses-{session}_magnitude.nii.gz'
                elif 'flywheel.json' in filename:
                    if session is None:
                        bids_name = f'sub-{sub_id}_fieldmap.json'
                    else:
                        bids_name = f'sub-{sub_id}_ses-{session}_fieldmap.json'
                else: 
                    if session is None:
                        bids_name = f'misc_sub-{sub_id}_fieldmap_{filename}'
                    else:
                        bids_name = f'misc_sub-{sub_id}_ses-{session}_fieldmap_{filename}'
            elif 'NEW Sag_MPRAGE_T1' in subdirectory: 
                new_subdirectory = 'anat'
                if '.nii.gz' in filename:
                    if session is None:
                        bids_name = f'sub-{sub_id}_T1w.nii.gz'
                    else:
                        bids_name = f'sub-{sub_id}_ses-{session}_T1w.nii.gz'
                else: 
                    if session is None:
                        bids_name = f'misc_sub-{sub_id}_anat_T1w_{filename}'
                    else:
                        bids_name = f'misc_sub-{sub_id}_ses-{session}_anat_T1w_{filename}'
            elif 'T2w CUBE PROMO' in subdirectory:
                new_subdirectory = 'anat'
                if '.nii.gz' in filename:
                    if session is None:
                        bids_name = f'sub-{sub_id}_T2w.nii.gz'
                    else: 
                        bids_name = f'sub-{sub_id}_ses-{session}_T2w.nii.gz'
                else:
                    if session is None:
                        bids_name = f'misc_sub-{sub_id}_anat_T2w_{filename}'
                    else:   
                        bids_name = f'misc_sub-{sub_id}_ses-{session}_anat_T2w_{filename}'
            elif 'task-localizer' in subdirectory:
                new_subdirectory = 'func'
                if '.nii.gz' in filename:
                    echo = filename.split('_')[3].split('e')[1].split('.')[0]
                    if session is None: 
                        bids_name = f'sub-{sub_id}_task-localizer_echo-{echo}_bold.nii.gz'
                    else:
                        bids_name = f'sub-{sub_id}_ses-{session}_task-localizer_echo-{echo}_bold.nii.gz'
                elif 'flywheel.json' in filename:
                    echo = filename.split('_')[3].split('e')[1].split('.')[0]
                    if session is None:
                        bids_name = f'sub-{sub_id}_task-localizer_echo-{echo}_bold.json'
                    else:
                        bids_name = f'sub-{sub_id}_ses-{session}_task-localizer_echo-{echo}_bold.json'
                else: 
                    if session is None:
                        bids_name = f'misc_sub-{sub_id}_func_localizer_{filename}'
                    else: 
                        bids_name = f'misc_sub-{sub_id}_ses-{session}_func_localizer_{filename}'
            elif 'task-rest' in subdirectory or 'task-vismot' in subdirectory or 'task-visloc' in subdirectory:
                new_subdirectory = 'func'
                if '.nii.gz' in filename:
                    task = subdirectory.split('-')[1].split('_')[0] 
                    run = subdirectory.split('_')[2]
                    echo = filename.split('_')[3].split('e')[1].split('.')[0]
                    if session is None:
                        bids_name = f'sub-{sub_id}_task-{task}_run-{run}_echo-{echo}_bold.nii.gz'
                    else:
                        bids_name = f'sub-{sub_id}_ses-{session}_task-{task}_run-{run}_echo-{echo}_bold.nii.gz' 
                elif 'flywheel.json' in filename:
                    task = subdirectory.split('-')[1].split('_')[0] 
                    run = subdirectory.split('_')[2]
                    echo = filename.split('_')[3].split('e')[1].split('.')[0]
                    if session is None:
                        bids_name = f'sub-{sub_id}_task-{task}_run-{run}_echo-{echo}_bold.json'
                    else:
                        bids_name = f'sub-{sub_id}_ses-{session}_task-{task}_run-{run}_echo-{echo}_bold.json'
                else: 
                    if session is None:
                        bids_name = f'misc_sub-{sub_id}_func_localizer_{filename}'
                    else:
                        bids_name = f'misc_sub-{sub_id}_ses-{session}_func_localizer_{filename}'
            else:
                continue 
            
            if '.nii.gz' in filename or 'flywheel.json' in filename:
                # rename to current subdirectory name
                # os.rename(filepath, os.path.join(directory, subdirectory, bids_name))
                # move file to new subdirectory
                if session is None:
                    print(f'{filepath} moved to {os.path.join(".", f"sub-{sub_id}", new_subdirectory, bids_name)}')
                    os.rename(filepath, os.path.join('.', f'sub-{sub_id}', new_subdirectory, bids_name))
                else:
                    print(f'{filepath} moved to {os.path.join(".", f"sub-{sub_id}", f"ses-{session}", new_subdirectory, bids_name)}')
                    os.rename(filepath, os.path.join('.', f'sub-{sub_id}', f'ses-{session}', new_subdirectory, bids_name))
            elif 'sidecars' in subdirectory:
                os.rename(filepath, os.path.join('.', f'sub-{sub_id}', f'ses-{session}', new_subdirectory, bids_name))
            else:
                # os.rename(filepath, os.path.join(directory, subdirectory, bids_name))
                if session is None:
                    print(f'{filepath} moved to {os.path.join(".", f"misc_sub-{sub_id}", bids_name)}')
                    os.rename(os.path.join(filepath), os.path.join('.', f'misc_sub-{sub_id}', bids_name)) 
                else:
                    print(f'{filepath} moved to {os.path.join(".", f"misc_sub-{sub_id}", f"ses-{session}", bids_name)}')
                    os.rename(os.path.join(filepath), os.path.join('.', f'misc_sub-{sub_id}', f'ses-{session}', bids_name))  

            # os.rename(filepath, os.path.join('.', f'sub-{sub_id}', new_subdirectory, bids_name))

    # change this part for the correct subject and directory name
    # rename_files(directory='sub-s002_ses-01', sub_id='02', file_path_num=2, session='1')
    # copy files from folder sidecars to create bids sidecar files
    rename_files(directory=args.directory, sub_id = args.subid, file_path_num=2, session=args.ses)
