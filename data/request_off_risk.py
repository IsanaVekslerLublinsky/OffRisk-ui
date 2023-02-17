import json
import os

import httpx
import pandas as pd
from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME_LIST = ['all']
SERVER_NAME = 'http://localhost:8123'
doi_10_1002_cti2_1372_input_FILE = f'{BASE_DIR}/doi_10_1002_cti2_1372.json'
doi_10_1002_cti2_1372_RESULT_FILE = f'{BASE_DIR}/doi_10_1002_cti2_1372_result.json'
LEENAY_INPUT_FILE_PATH = f'{BASE_DIR}/Leenay_pam_alignment.tsv'
LEENAY_INPUT_JSON_FILE_PATH = f'{BASE_DIR}/Leenay_pam_alignment.json'
LEENAY_RESULT_FILE_PATH = f'{BASE_DIR}/Leenay_pam_alignment_result.json'


def handle_post_request(json_as_dictionary, str_of_target, server=SERVER_NAME):
    '''
    :param server: the server name or IP to send the request to
    :param json_as_dictionary: the user input in json format
    :param str_of_target: off-target / on-target
    :return: response from the server
    '''

    r = httpx.post('{}/v1/{}-analyze/'.format(server, str_of_target), timeout=10000,
                   json=json_as_dictionary)

    if r.status_code == 200:
        print('Server returned code: {}'.format(r.status_code))
        return r.json()
    else:
        print('Server returned error code: {}: {}'.format(r.status_code, r.text))


def on_target_doi_10_1002_cti2_1372_request():
    request_body = [{
        'request_id': 1,
        'sites': [
            {
                'sequence': 'GGAGAATGACGAGTGGACCC'
            }
        ],
        'search_tools': ['cas_offinder', 'flashfry']
    },{'request_id': 2,
        'sites': [
            {
                'sequence': 'GAGAATCAAAATCGGTGAATAGG'
            }
        ],
        'search_tools': ['cas_offinder', 'flashfry']}]
    result_list = list()
    for request in request_body:
        on_target_response = handle_post_request(request, 'on-target', SERVER_NAME)
        result_list.append(on_target_response)
    with open(doi_10_1002_cti2_1372_RESULT_FILE, 'w') as f:
        json.dump(result_list, f)


def create_leenay_site_list_json():
    leenay_pam_alignment_df = pd.read_csv(LEENAY_INPUT_FILE_PATH, sep='\t')
    leenay_pam_alignment_df['gRNA'] = leenay_pam_alignment_df.apply(lambda row: ''.join([row['protospacer'],
                                                                                         row['pam']]), axis=1)
    site_list = list()
    for row in leenay_pam_alignment_df.itertuples():
        site = {
            'sequence': row.gRNA,
            'upstream': '',
            'downstream': ''
        }
        site_list.append(site)
    print('total number of sites: {}'.format(len(site_list)))
    with open(LEENAY_INPUT_JSON_FILE_PATH, 'w') as outfile:
        json.dump(site_list, outfile)
    return site_list


def on_target_leenay_site():
    site_list = create_leenay_site_list_json()
    result_response_list = list()

    for i in tqdm(range(0, len(site_list), 40)):
        request_body = {
            'request_id': i,
            'sites': site_list[i:i + 40]}

        on_target_response = handle_post_request(request_body, 'on-target', SERVER_NAME)
        result_response_list.append(on_target_response)

    with open(LEENAY_RESULT_FILE_PATH, 'w') as f:
        json.dump(result_response_list, f)


def load_result_to_df(result_file):
    with open(result_file, 'r') as f:
        results = json.load(f)
    off_target_df, flashfry_score_df, gendoce_df, mirgene_df, remapepd_df, enhanceratlas_df, pfam_df, targetscan_df, \
    omim_df, humantf_df, protein_atlas_df, rbp_df, cosmic_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), \
                                                               pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), \
                                                               pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), \
                                                               pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), \
                                                               pd.DataFrame()

    for result in results:
        if result:
            if result.get('off_targets'):
                new_db = pd.DataFrame.from_dict(result['off_targets'])
                new_db['request_num'] = result['request_id']
                off_target_df = pd.concat([off_target_df, new_db])
            if result.get('flashfry_score'):
                new_db = pd.DataFrame.from_dict(result['flashfry_score'])
                new_db['request_num'] = result['request_id']
                flashfry_score_df = pd.concat([flashfry_score_df, new_db])
            if result.get('all_result', {}).get('GENCODE_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['GENCODE_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                gendoce_df = pd.concat([gendoce_df, new_db])
            if result.get('all_result', {}).get('MirGene_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['MirGene_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                mirgene_df = pd.concat([mirgene_df, new_db])
            if result.get('all_result', {}).get('EnhancerAtlas_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['EnhancerAtlas_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                enhanceratlas_df = pd.concat([enhanceratlas_df, new_db])
            if result.get('all_result', {}).get('ReMapEPD_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['ReMapEPD_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                remapepd_df = pd.concat([remapepd_df, new_db])
            if result['all_result']['Pfam_result_list']:
                new_db = pd.DataFrame.from_dict(result['all_result']['Pfam_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                pfam_df = pd.concat([pfam_df, new_db])
            if result.get('all_result', {}).get('TargetScan_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['TargetScan_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                targetscan_df = pd.concat([targetscan_df, new_db])
            if result.get('all_result', {}).get('OMIM_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['OMIM_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                omim_df = pd.concat([omim_df, new_db])
            if result.get('all_result', {}).get('HumanTF_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['HumanTF_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                humantf_df = pd.concat([humantf_df, new_db])
            if result.get('all_result', {}).get('Protein_Atlas_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['Protein_Atlas_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                protein_atlas_df = pd.concat([protein_atlas_df, new_db])
            if result.get('all_result', {}).get('RBP_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['RBP_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                rbp_df = pd.concat([rbp_df, new_db])
            if result.get('all_result', {}).get('COSMIC_result_list'):
                new_db = pd.DataFrame.from_dict(result['all_result']['COSMIC_result_list'][0]['data'])
                new_db['request_num'] = result['request_id']
                cosmic_df = pd.concat([cosmic_df, new_db])

    off_target_df.to_csv(f'{result_file}_off_target_df.csv', sep='\t', index=False)
    flashfry_score_df.to_csv(f'{result_file}_flashfry_score_df.csv', sep='\t', index=False)
    gendoce_df.to_csv(f'{result_file}_gendoce_df.csv', sep='\t', index=False)
    mirgene_df.to_csv(f'{result_file}_mirgene_df.csv', sep='\t', index=False)
    remapepd_df.to_csv(f'{result_file}_remapepd_df.csv', sep='\t', index=False)
    enhanceratlas_df.to_csv(f'{result_file}_enhanceratlas_df.csv', sep='\t', index=False)
    pfam_df.to_csv(f'{result_file}_pfam_df.csv', sep='\t', index=False)
    targetscan_df.to_csv(f'{result_file}_targetscan_df.csv', sep='\t', index=False)
    omim_df.to_csv(f'{result_file}_omim_df.csv', sep='\t', index=False)
    humantf_df.to_csv(f'{result_file}_humantf_df.csv', sep='\t', index=False)
    protein_atlas_df.to_csv(f'{result_file}_protein_atlas_df.csv', sep='\t', index=False)
    rbp_df.to_csv(f'{result_file}_rbp_df.csv', sep='\t', index=False)
    cosmic_df.to_csv(f'{result_file}_rbp_df.csv', sep='\t', index=False)
    print('Done')


def main():
    # on_target_leenay_site()
    # load_result_to_df(LEENAY_RESULT_FILE_PATH)

    on_target_doi_10_1002_cti2_1372_request()
    load_result_to_df(doi_10_1002_cti2_1372_RESULT_FILE)


if __name__ == '__main__':
    main()
