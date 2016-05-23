BEGIN{
	val = 0; 
	nb = 0 ;
	for(i=1 ; i<=NB_OF_COLS ; i=i+1)
	{
		cumul[i] = 0;
	}
}
{
	# Offsets if we have a comment or not
	#print $1 " " $2 " " $3 " " $4 " " $5 " " $6 " " $7 " " $8 " " $9"-->nb=" nb "\n";
	#print "prev1: " previous1 ", val: " $1 "\n";

	#printf("->  %d %d %d | %d\n", NF == NB_OF_COLS, NF, NB_OF_COLS, NB_FIXED_COLS);

	#a correct nb of columns
	if (NF == NB_OF_COLS)
	{
		#this corresponds to a new group of values, print it
		if ((nb != 0) && (previous1 != $1))
		{
			flush_values() ;
		}
		
		#I am storing the sum values for each column
		for(i=0 ; i<NF ; i=i+1)
		{
			cumul[i] = cumul[i] + $(i+1);
			tab[nb*NF + i] = $(i+1);
		}    
   
		#to detect group frontiers
		previous1 = $1 ;
		nb = nb + 1;
 	}
 	else{
 		#print "some lines have an incorrect nb of columns(" NF ") compared to " NB_OF_COLS;
 	}
 }

#I must print the last stored value
END{
	flush_values() ;
}


#returns the power nb
function pow(val , expo)
{
	return exp(expo * log(val));
}

#absolute value
function abs(a)
{
	if (a < 0)
	return -a;
	return a;
}
#print the cumulated values for all the columns
function flush_values()
{
	str_av="";
	str_conf_sup="";
	str_conf_inf="";
	
	#nb=0 means probably that we are dealing with an empty file (no value -> nothing to compute)
	if (nb != 0)
	{
		for(i=0 ; i<NB_OF_COLS ; i=i+1)
		{

			#average value
			str_av=str_av cumul[i]/nb "	";
       
			#standard deviation
			std_dev=0;
			for(j=0; j<nb ; j++)
			{
				std_dev = std_dev + pow(abs(cumul[i]/nb - tab[i + j* NB_OF_COLS]), 2);
				#if (i == 4){
				#	print "avg " cumul[i]/nb " value " tab[i + j* NB_OF_COLS] " std dev " std_dev;
				#}
			}
			std_dev = pow( std_dev / nb , 0.5)
		
        
			#confidence interval
			if (i>=NB_FIXED_COLS)
			{			
				str_conf_sup=sprintf("%s%g	", str_conf_sup , cumul[i]/nb + (1.96 * std_dev / sqrt(nb)));
				str_conf_inf=sprintf("%s%g	", str_conf_inf , cumul[i]/nb - (1.96 * std_dev / sqrt(nb)));
			}
			else
			#for the NB_FIXED_COLS first columns, print only the average value 
			#NB: these are parameters, used only for x-coordinates
			{
				str_conf_sup=sprintf("%s%g	", str_conf_sup , cumul[i]/nb);
				str_conf_inf=sprintf("%s%g	", str_conf_inf , cumul[i]/nb);
			}
			#reset the sum
			cumul[i] = 0 ;
		}
	}
	print str_av;
	print str_conf_sup;
	print str_conf_inf;
	print str_av;
	nb = 0 ;
}
