import pandas as pd

# Load existing barcodes
barcodes = pd.read_csv('barcode.csv')
cattle_muts = pd.read_csv('data/cattle_base.tsv', sep='\t', header=None, index_col=0)

cattle_root = cattle_muts.loc['nuc_changes'].values[0].split(', ')
cattle_reversions = cattle_muts.loc['nuc_reversionsToRoot'].values[0].split(', ')

print(cattle_root)
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
    #'A.1.6': cattle_root + ['T1338A', 'A448G'] Omitted for now because of spurious detection in samples with low coverage at 448
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