program main
! quick program to calculate the phase difference of two files
! Call with [program] [file1] [file2] [1 for phase, 0 for res]
! Input: two sigma files, one high, one low
! Output: a sigma file named from both files, with some math performed on them
! 
! You may need to edit the values for the sstarting model



implicit none


integer :: LUH1, LUH2, LUHOUT
character(len=256) :: file1, file2, fileout, arg3, arg4
integer :: i, nele, nele2, phase, abs_opt
real    :: val1_f1, val2_f1, val1_f2, val2_f2


! ---------------------------------------------------------
! Quick variable definitions
IF(iargc().lt.3) then
  write(*,*) "Not enough arguments! Please input both an input filename &
  & and output filenames, then 1 for phase or 0 for res VOI as arguments. Exiting"
  STOP
END IF

call GETARG(1,file1)
call GETARG(2,file2)
call GETARG(3,arg3)
read(arg3, *) phase

!absolute value option
if(iargc()>3) then 
  call GETARG(4,arg4)
  read(arg4,*) abs_opt 
else
  abs_opt=0
end if
if(abs_opt.eq.1) then
  fileout="VOI_abs_"//file2(:len_trim(file2)-4) //"_minus_" // file1
else
  fileout="VOI_non-abs_"//file2(:len_trim(file2)-4) //"_minus_" // file1
end if

LUH1=99
LUH2=98
LUHOUT=97

! ---------------------------------------------------------
! Opening files
write(*,*) "Opening files. Filenames:"
write(*,*) "    Input1: ", trim(file1)
write(*,*) "    Input2: ", trim(file2)
write(*,*) "    Output: ", trim(fileout)
open(unit=LUH1, file=file1, ACCESS='sequential', status='old' )
open(unit=LUH2, file=file2, ACCESS='sequential', status='old' )
open(unit=LUHOUT, file=fileout, ACCESS='sequential', status='unknown' )



! ---------------------------------------------------------
! doing the math
write(*,*) "Reading inputs and writing output VOI on the fly..."
read(LUH1,*) nele
read(LUH2, *) nele2
if(nele.ne.nele2) then
  write(*,*) "ERROR! Sigma files do not match up. Ensure they came from the same mesh and retry"
  STOP
end if

write(LUHOUT, *) nele, 2


if(phase.eq.1) then
  write(*,*) " Calculating Phase VOI..."
  do I=1, nele
    read(LUH1, *) val1_f1, val2_f1
    read(LUH2, *) val1_f2, val2_f2
    if(abs_opt.eq.1) then
      write(LUHOUT, *) abs(log10(atan(val2_f2/val1_f2))-log10(atan(val2_f1/val1_f1))), &
                    & abs((atan(val2_f2/val1_f2)-atan(val2_f1/val1_f1))/(0.014-0.035) )
    else
      write(LUHOUT, *) log10(atan(val2_f1/val1_f1))-log10(atan(val2_f2/val1_f2)), &
                    & (atan(val2_f2/val1_f2)-atan(val2_f1/val1_f1))/(0.014-0.035)
    end if
  end do
else 
  write(*,*) " Calculating RES VOI..."
  do I=1, nele
    read(LUH1, *) val1_f1
    read(LUH2, *) val1_f2
    val1_f1 = 1.0/val1_f1
    val1_f2 = 1.0/val1_f2
    if(abs_opt.eq.1) then
      write(LUHOUT, *) abs(log10(val1_f1)-log10(val1_f2))  &
                    &, abs( (val1_f2-val1_f1)/(1.0/0.0008-1.0/0.08) )
    else
      write(LUHOUT, *) (log10(val1_f1)-log10(val1_f2))  &
                    &,  (val1_f2-val1_f1)/(1.0/0.0008-1.0/0.08)       
    end if
  end do
end if

write(*,*) "Done! Closing files and exiting..."
! ---------------------------------------------------------
! cleanup, closing files
 close(LUH1)
 close(LUH2)
 close(LUHOUT)










end program
