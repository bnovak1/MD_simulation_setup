proc split_LACT_chains {infile outprefix} {

    set basemol [mol new $infile]

    set sel [atomselect $basemol "resname LACT"]
    set chainlist [lsort -unique -integer [$sel get fragment]]
    $sel delete

    foreach chain $chainlist {
        set sel [atomselect $basemol "fragment $chain"]
        $sel writepdb ${outprefix}${chain}.pdb
        $sel delete
    }

}
