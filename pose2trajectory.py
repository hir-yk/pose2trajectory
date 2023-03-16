#!/usr/bin/env python3

import numpy as np
import quaternion
import argparse
import sys

INFILE='rostopic_echo.csv'
OUTFILE='trajectory.csv'
TH_DISTANCE=1.0


def main(infile, outfile, th_dist):
    traj=[]
    last_x, last_y=0.0, 0.0

    with open(infile, 'r') as f:
        for line in f:
            l=line.strip().split(",")
            dat=list(map(lambda x: float(x), l[3:]))
            q=np.quaternion(dat[3],dat[4],dat[5],dat[6])  # why this order?
            yaw=quaternion.as_euler_angles(q)[1]

            x,y,z=dat[0:3]
            dist=((x-last_x)**2 + (y-last_y)**2)**0.5
            if( dist > th_dist ): 
                traj.append((x,y,z,yaw))
                last_x=x
                last_y=y

    np.savetxt(outfile, traj, fmt='%.5f', delimiter=',', header='x,y,z,yaw', comments='')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        usage='pose2trajectory.py <infile> [options]',
        description='description',
        epilog='end',
        add_help=True,
        )

    parser.add_argument('infile', default='infile.csv', help="input file: result of 'ros2 topic echo --csv <topicname>'")
#    parser.add_argument('outfile', type=argparse.FileType('w'), default='outfile.csv', help="output file: trajectory format for VectorMapBuilder", required=False)


#    parser.add_argument('-i', '--infile', help="input file: result of 'ros2 topic echo --csv <topicname>'", required=False, default=INFILE)
    parser.add_argument('-o', '--outfile', help="output file: trajectory file(.csv) for VectorMapBuilder", required=False, default='output.csv')
    parser.add_argument('-i', '--interval', help="interval for creating waypoints [m]", required=False, type=float, default=TH_DISTANCE)
    args = parser.parse_args()

    main(args.infile, args.outfile, args.interval)

