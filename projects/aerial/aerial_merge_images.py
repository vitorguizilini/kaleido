
import numpy as np
import kaleido as kld

######################

def draw( recimage , reclabel , recoutput ):
    imglbl , imgout = recimage.copy() , recimage.copy()
    imglbl[:,:,2] , imgout[:,:,2] = reclabel , recoutput
    recerror = np.square( reclabel - recoutput )
    return kld.plt.block( 2 , 3 , [ recimage , reclabel  , imglbl ,
                                    recerror , recoutput , imgout ] )

######################

parser = kld.mng.Parser( 'Image Merger for Aerial' )

parser.add_int(  'idx'     , d = 6                   , h = 'Index to be reconstructed')
parser.add_str(  'path'    , d = 'aerial/cerrado'    , h = 'Path to data' )
parser.add_str(  'dataset' , d = '5_128_128_nearest' , h = 'Dataset name' )
parser.add_lstr( 'output'  , d = [ 'versionA/trained01' , 'training' ] ,
                                                       h = 'Output to be used' )
args = parser.args()

######################

path_rcimg = '../../data/%s_%s/images/%02d' % ( args.path , args.dataset , args.idx )
path_rclbl = '../../data/%s_%s/labels/%02d' % ( args.path , args.dataset , args.idx )
path_rcout = '../../logs/%s/%s/images/%s/individual/valid' % (
                    args.path , args.output[0] , args.output[1] )

scl , cx , cy = args.dataset.split('_')[:3]
scl , cx , cy = int( scl ) , int( cx ) , int( cy )
hx , hy = int( cx / 2 ) , int( cy / 2 )

loader = kld.log.Saver( '../../data/%s_%s' % ( args.path , args.dataset ) , free = True )
dims = loader.list( 'dims' )[0]; nx , ny = int( dims[0] ) , int( dims[1] )
shape = [ hx * nx , hy * ny ]

recimage  = np.zeros( shape + [3] , dtype = np.float32 )
reclabel  = np.zeros( shape       , dtype = np.float32 )
recoutput = np.zeros( shape       , dtype = np.float32 )

h , w , _ = recimage.shape
kld.plt.adjust( w = 20 , p = h / w / 1.5 )
saver = kld.log.Saver( path_rcout + '_rec' , free = True )
saver.restart()

files_rcimg = kld.mng.Folder( path_rcimg ).files( pat = '*.png' )
recimages = kld.img.load( files_rcimg , 'rgbn'  )
files_rclbl = kld.mng.Folder( path_rclbl ).files( pat = '*.png' )
reclabels = kld.img.load( files_rclbl , 'grayn'  )

folders_rcout = kld.mng.Folder( path_rcout , recurse = 1 )

for k in range( 200 ):

    str = '*_%04d_out.png' % k
    files_rcout = folders_rcout.files( pat = str )

    if len( files_rcout ) > 0:

        recoutputs = kld.img.load( files_rcout , 'grayn' )
        print( '### CREATING %s idx %s from %s on %s for Epoch %04d' % (
                        args.path , args.idx , args.dataset , args.output[0] , k ) )

        cnt = 0
        for i in range( nx - 1 ):
            for j in range( ny - 1 ):
                stx , sty = i * hx , j * hy
                fnx , fny = stx + cx , sty + cy
                recimage[  stx : fnx , sty : fny ] = recimages[cnt]
                reclabel[  stx : fnx , sty : fny ] = reclabels[cnt]
                recoutput[ stx : fnx , sty : fny ] = recoutputs[cnt]
                cnt += 1

        saver.image( 'plot' , draw( recimage , reclabel , recoutput ) ,
                                         'merge_%03d_%02d' % ( k , args.idx ) )
        saver.image( 'raw' , recimage  , 'image_%02d' % ( args.idx ) )
        saver.image( 'raw' , reclabel  , 'label_%02d' % ( args.idx ) )
        saver.image( 'raw' , recoutput , 'output_%03d_%02d' % ( k , args.idx ) )


