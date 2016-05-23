BEGIN{
}
{
	# the parameter (will be the first column)
	line = "";
	line = sprintf("%.8f\t", $(COL_PARAM));
	
	#other values (except the parameter)
	for(i=1 ; i<=NF ; i=i+1)
	{
		if (i != COL_PARAM)
			line = sprintf("%s\t%s" , line, $(i));

		#special debug
		#if (i == 19)
		#	line = sprintf("%s\t%s" , line, $(i));
	}
	
	
	#print each line
	if (NF > 1)
		printf("%s\n",line);
}
END{
}
