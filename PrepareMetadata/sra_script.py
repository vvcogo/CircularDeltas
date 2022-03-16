import pandas as pd
from collections import defaultdict
import os
import shutil
import sys

#put every model from the Ion Torrent platform in the same pattern
def create_pattern_ion_torrent(row):
    model =getattr(row,"Model")
    model_first_word = model.split(' ')[0]
    if len(model.split(' ')) > 1:
        model_second_word = model.split(' ')[1]
        if model_first_word == "Ion" and model_second_word != "Torrent":
            rest_of_model = model[model.index(model.split(' ')[1]):]
            model_result = "Ion Torrent" + " "+ rest_of_model
        elif model_first_word == "Ion" and model_second_word == "Torrent":
            model_result = model
    else:
        model_second_word = model[model.index(model.split(' ')[0]):]
        model_result = "Ion Torrent" + " " + model_second_word

    return model_result

#put every model from each platform in the same pattern
def create_pattern_models(file,changes_models_dict,platform_model_dict):
    aux = []
    for row in file.itertuples(index = False):
        platform = getattr(row,"Platform")
        model = getattr(row,"Model")
        run = getattr(row,"Run")
        spots = getattr(row,"spots")
        whitespace = model.find(' ')
        model_before_whitespace = model[:whitespace]
        if platform == "ION_TORRENT":
            model_result = create_pattern_ion_torrent(row).strip()
            aux.append([platform,model_result,run])

            #if model_result not in changes_models_dict:
            #    changes_models_dict[model_result] = model
            if model_result not in changes_models_dict:
                changes_models_dict[model_result] = [model]
            changes_models_dict[model_result].append([run,spots])

        if platform in platform_model_dict and model_before_whitespace in platform_model_dict.values():
            model_result = model.strip()
            aux.append([platform,model_result,run])

            #if model_result not in changes_models_dict:
            #    changes_models_dict[model_result] = model
            if model_result not in changes_models_dict:
                changes_models_dict[model_result] = []
            changes_models_dict[model_result].append([run,spots])

        elif platform in platform_model_dict:
            model_result =(platform_model_dict[platform] + " " + model).strip()
            aux.append([platform,model_result,run])

            #if model_result not in changes_models_dict:
            #    changes_models_dict[model_result] = model
            if model_result not in changes_models_dict:
                changes_models_dict[model_result] = []
            changes_models_dict[model_result].append([run,spots])

    df_aux = pd.DataFrame(aux,columns = ['Platform','Model','Run'])
    return df_aux

#create a directory for each platform
def create_dir(file):
    if not os.path.exists(file):
        os.makedirs(file)

def delete_dir(primary_path):
    #for deleting the results that we created using the argument -d
    #if len(argv) > 0 and argv[0] == '-d':
        if os.path.exists(primary_path):
                try:
                    shutil.rmtree(primary_path)
                except OSError as e:
                    print("Error deleting: %s"%primary_path)

def create_files(primary_path,names_dict,changes_models_dict):

    #import the csv files
    count_df = pd.read_csv(os.path.join(primary_path,'SraRunInfoCount.csv'))

    #goes through the count file and the models and saves the path in the names_dict associating with the model and create a list in the changes_models_dict associating with the model and create the directories for the platforms
    for row in count_df.itertuples(index = False):
        model =getattr(row,"Model")
        platform = getattr(row,"Platform")
        path =os.path.join(primary_path,"%s"%platform)
        create_dir(path)
        name = model.replace(' ','_')
        complete_name = os.path.join(path,name)
        names_dict[model] = complete_name

    #putting the changes_models_dict into a file
    with open(os.path.join(primary_path,'changes_models_dict.txt'), 'w') as f:
        for key, value in changes_models_dict.items():
            f.write('%s:%s\n' % (key, value))

    #goes through the changes_models_dict to create a file for each model creating a csv file
    for key,value in changes_models_dict.items():
        df = pd.DataFrame(value,columns = ['Run','spots'])
        df.to_csv('%s.csv' %names_dict[key],index = False)


def main(args):
    #creating the main directory
    #the output is placed in the directory passed as argv[1]
    primary_path = args[1]

    delete_dir(primary_path)

    #runing the script normaly to create the results
    create_dir(primary_path)
    #the platform as the keys and the beggining of the models as values
    platform_model_dict = {'ABI_SOLID':'AB','BGISEQ':'','CAPILLARY':'AB','COMPLETE_GENOMICS':'Complete','HELICOS':'Helicos','ILLUMINA':'Illumina','LS454':'454','OXFORD_NANOPORE':'','PACBIO_SMRT':'PacBio'}
    #the models after the changes as the keys and before the changes as the values
    changes_models_dict = {}
    #the models alredy changed and with no repeated as keys and the list with the run and spots as the values
    changes_models_dict = defaultdict(list)
    #the models alredy changed as the keys and the names of the files( the path with the directory also) as the values
    names_dict = {}

    #the input CSV file is the one passed as argv[0]
    df = pd.read_csv (args[0])
    #getting the platform,model,run and spots
    filtered_df = df.iloc[:,[0,3,18,19]]
    #excluding the  rows names that apear in the middle of the file
    final_filtered_df = filtered_df[(filtered_df["Platform"] != "Platform")]
    final_filtered_df.to_csv(os.path.join(primary_path,'SraRunInfoReturn.csv'), index=False)

    #make a csv file with the count of every model without the repeated ones
    final_count = create_pattern_models(filtered_df,changes_models_dict,platform_model_dict).groupby(['Platform','Model']).count()
    final_count.to_csv(os.path.join(primary_path,'SraRunInfoCount.csv'))

    create_files(primary_path,names_dict,changes_models_dict)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1:])
    else:
        print('Usage: python3 sra_script.py <input_CSV> <output_dir>')
        sys.exit(1)
