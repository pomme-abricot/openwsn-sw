{
	val1 = pow(sqrt($1), 2);
	val2 = pow(sqrt($2), 2);
	
	if (val1 > val2)
		print "1";
	else if (val1 < val2)
		print "-1";
	else
		print "0";
}
#returns the power nb
function pow(val , expo)
{
	return exp(expo * log(val));
}