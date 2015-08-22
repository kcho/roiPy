import nibabel as nb
import os
import numpy as np
import argparse
import textwrap



def main(args):
    f = nb.load(args.inputImg)

    data = f.get_data()
    loc = args.coordinate

    #print data.shape

    roiDf = np.zeros(data.shape)
    roiDf[loc] = 1
    new_roiData = nb.Nifti1Image(roiDf, f.affine)
    new_roiData.to_filename('new_roi.nii.gz')

    #command = 'fslmaths new_roi.nii.gz -dilD -dilD another_roi.nii.gz -odt float'

    #os.popen(command).read()
    #fslmaths ACCpoint -kernel sphere 5 -fmean ACCsphere -odt float


    f = nb.load('another_roi.nii.gz')
    roiData = f.get_data()

    data[roiData==1] =  data[roiData==1] - 200

    newData = nb.Nifti1Image(data, f.affine)
    newData.to_filename('final_T1.nii.gz')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            {codeName} : Changes image intensity. 
            Used in CCNC workshop test.
            ========================================
            eg) {codeName} -i T1.nii.gz 
            eg) {codeName} -i T1.nii.gz -k 10
            eg) {codeName} -i T1.nii.gz -c 130 100 50
            '''.format(codeName=os.path.basename(__file__))))

    parser.add_argument(
        '-i', '--inputImg',
        help = 'Data directory location, default=pwd')

    parser.add_argument(
        '-c', '--coordinate',
        help = 'coordinate of the voxel center to change',
        nargs = '+',
        default = [150, 133, 85])

    parser.add_argument(
        '-k', '--kernel',
        help ='sphere kernel size',
        default=5)
        
    parser.add_argument(
        '-o', '--outImg',
        help = 'output image',
        default = 'output.nii.gz') 

    args = parser.parse_args()

    if not args.inputImg:
        parser.error('No input image is given, add -i or --imageImg')

    main(args)
