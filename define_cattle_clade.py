import pandas as pd

# Load existing barcodes
barcodes = pd.read_csv('barcode.csv')

cattle_root = 'A12C, A30C, G36A, T39A, C54T, C102T, A105G, G114A, A123G, C126A, G174A, C192A, T198C, A207G, T216A, A219G, A228G, T231C, T234C, T270C, A284G, T285A, A313C, A314G, C318T, T321C, C327T, A350G, T351C, T352C, C357T, T360C, C379A, A381G, C396T, A408G, C420T, A426G, T432C, T436C, C438A, G439A, G448A, C450A, T454C, C455T, A459G, T466G, A471T, C474T, A486G, G489A, T490C, A513G, A532G, A554T, C557G, C570T, C573T, A575G, A576G, T585C, C606T, C610T, T612C, T615C, G616A, C623A, G635A, G636T, T642C, C643A, C653T, T660C, C666A, G672A, A681T, C682T, A693G, T698C, C711T, A721C, A736C, G750C, T765C, G774A, A775G, A787C, C789T, T801C, C840T, A855G, A872G, T874G, T885C, A886C, C888T, G900A, G906A, T909C, A913G, G918T, C927T, C942T, C954T, C966T, T984C, A999G, A1002G, A1014T, C1029T, A1034T, G1041A, G1043A, A1044G, A1062T, A1065G, A1071G, T1074G, A1113T, C1134T, A1167G, T1182C, C1203T, G1221A, G1245A, T1254A, A1266G, A1287G, A1299G, G1308A, G1320A, T1338C, G1356A, T1371C, A1377G, C1386T, C1395T, G1422A, C1426A, C1429T, T1464C, T1467C, G1476A, A1515G, C1521T, A1524G, A1539T, G1572A, T1581C, A1587G, G1593A, A1600G, A1614G, T1637C, G1641A, G1666A, A1728G, G1733A, T1738C'
cattle_root = cattle_root.replace(' ', '').split(',')
cattle_reversions = 'C195C, C199C, T300T, A413A, G488G, A939A, C948C, A990A, G1083G, C1416C, A1431A, T1491T, A1710A'
cattle_reversions = cattle_reversions.replace(' ', '').split(',')
cattle_reversions = [int(mutation[1:-1]) for mutation in cattle_reversions]

# New lineages:
new_lineages = {
    'A': cattle_root,
    'A.1': cattle_root + ['T1338A'],
    'A.1.1': cattle_root + ['T1338A', 'T300G', 'G684A'],
    'A.1.2': cattle_root + ['T1338A', 'A487G', 'G488C', 'G1299A'],
    'A.1.3': cattle_root + ['T1338A', 'T1732C'],
    'A.1.4': cattle_root + ['T1338A', 'G921A', 'G1374A'],
    'A.1.5': cattle_root + ['T1338A', 'G1071A'],
    #'A.1.6': cattle_root + ['T1338A', 'A448G']
} 

template = barcodes[barcodes['Unnamed: 0'] == 'H5Nx-2.3.4.4b']
for column in template.columns:
    if column == 'Unnamed: 0':
        continue
    if int(column[1:-1]) in cattle_reversions:
        template[column] = 0.0

# Add new lineages to index column as a copy of template
# Then add the mutations to the barcode column
new_barcodes = []
for lineage in new_lineages.keys():
    print(lineage, new_lineages[lineage])
    new_lineage = template.copy()
    new_lineage['Unnamed: 0'] = f'H5Nx-{lineage}'
    for mutation in new_lineages[lineage]:
        if mutation in barcodes.columns:
            new_lineage[mutation] = 1.0
        else:
            barcodes[mutation] = 0.0
            new_lineage[mutation] = 1.0

    new_barcodes.append(new_lineage)

barcodes = pd.concat([barcodes, pd.concat(new_barcodes)])

barcodes= barcodes.fillna(0.0)
barcodes.to_csv('cattle_barcode.csv', index=False)