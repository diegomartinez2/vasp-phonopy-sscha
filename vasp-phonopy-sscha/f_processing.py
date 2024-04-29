#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import re
from glob import glob
import numpy as np

def f_processing(parsed_args,atom_occurrencies,type_atoms):
    pop_id = parsed_args[0][0]
    n = parsed_args[0][1]
    all_files = glob("vasp/forces/*")
    all_files.sort(key=lambda f: int(re.sub('\D', '', f)))
    a = 0
    for file in all_files:
        a = a + 1
        print(file)
        #forces = pd.read_csv(file, engine='python', sep="\s+", skiprows=1, header=None)
        forces = pd.read_csv(file, engine='python', sep="\s+", skiprows=1, header=None, nrows=81) #new VASP code also write stress
        #df_2 = forces.iloc[(forces.loc[forces[0]=='<varray name="stress" >'].index[0]+1):, :].reset_index(drop = True)
        forces.drop([0, 4], axis=1, inplace=True)

        forces = forces * 0.0388937935
        #forces = forces.apply(lambda x: x*0.388937935)

        processed_forces_path = f"data/forces_population{pop_id}_" + str(a) + ".dat"
        f = open(processed_forces_path, "w+")

        N = int(n)*int(n)*int(n)

        for i in range(0, N):
            for j in range(len(type_atoms)):
                for jj in range(0,int(atom_occurrencies[j])):
                    print("[",atom_occurrencies[j]*i+j*N+jj,"]")
                    force =  forces.iloc[atom_occurrencies[j]*i+j*N+jj] #this do not work nicely (need to be fixed to a generic way to relocate the indexes)
                    force = force.to_frame()
                    force = force.transpose()
                    #force = force *0.0388937935
                    force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
# Test the creation of a list for the reordenation of atoms
        for i in range(N):
            for j in range(len(type_atoms)):
                for k in range(int(atom_occurrencies[j])):
                    print("[",atom_occurrencies[j]*i+k,"]")
