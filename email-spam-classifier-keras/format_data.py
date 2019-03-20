import os
import pandas as pd
import eml_parser
from bs4 import BeautifulSoup

"""
Extracts .eml data from spicifed path.

Args:
    path: dir to look for data
    training_set: adds label otherwise extracts other features
"""


def format_email_data(path, training_set=True):
    data = os.listdir(path)
    data_extract = []

    if training_set:
        #read in training labels and map to training data durring extraction.
        training_labels = pd.read_csv('./challenge-data/spam_label_tr.csv')

    for idx, file in enumerate(data):
        f = open(path+file, "rb")
        raw_email = f.read()

        try:
            #use eml_parser to parse metadata from email
            parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

            _from = parsed_eml['header']['from']
            subject = parsed_eml['header']['subject']
            sample_number = file.split('_')[1].split('.')[0]


            if training_set:
                body_stream = open(f'./challenge-data/eml-body-data-train/{file}',"rb")
                body = body_stream.read()
            else:
                body_stream = open(f'./challenge-data/eml-body-data-test/{file}',"rb")
                body = body_stream.read()






            body_stream.close()



            if training_set:

                label_row = training_labels.loc[training_labels['Id'] == int(sample_number)]
                pred = label_row['Prediction'].get_values()[0]
                data_extract.append([int(sample_number),subject,_from, body, pred])


            else:
                 data_extract.append([int(sample_number),subject,_from, body])

        except ValueError as e:
            print("Error skipping file in extraction: " + str(e))
            print(body)
            break
        except Exception as e:
            print('Skipping file in extraction unknown error', str(e))


        f.close()


        print(str(round((idx/len(data)) * 100)) + "% done")

    return data_extract


#creates train and test dataset in csv format
formatted_training_data = pd.DataFrame(format_email_data('./challenge-data/TR/'),columns=['ID', 'subject','from','body' ,'prediction'])
formatted_training_data.to_csv('train_data_body.csv')


formatted_test_data = pd.DataFrame(format_email_data('./challenge-data/TT/', training_set=False),columns=['ID', 'subject', 'from', 'body'])
formatted_test_data.to_csv('test_data_body.csv')
