#!/usr/bin/awk -f

BEGIN {
	# printf("%s\n", "Hello world!");
	keyword["*HEAD"] = 1;
	keyword["*ELEMENTS"] = 2;
	keyword["*SPECIES"] = 3;
	keyword["*REACTION SYSTEM"] = 4;
	keyword["*INITIAL CONCENTRATIONS"] = 5;
	keyword["*TEMPERATURE"] = 6;
	keyword["*GAS CONSTANT"] = 7;
	keyword["*NUMERICAL INPUT"] = 8;
	keyword["*ACCURACY"] = 9;
	keyword["*OUTPUT POINTS"] = 10;
	keyword["*PRINT PARAMETER"] = 11;
	keyword["*MEASUREMENTS"] = 12;
}


/^\*HEAD/ {
	e = getline;
	printf("%s:%s \"%s\"\n", 
	       "@model", "3.1.1=HEAD", trim($0));
	while ( !($0 in keyword))
	{
		# printf("%4d: %s\n", NR, $0);
		e = getline;
	}
	
	compart[1] = "cell";
	printf("%s\n", "@compartments");
	printf(" %s=%f\n", compart[1], 1.0);
}


/^\*ELEMENTS/ {
	e = getline;
	while ( !($0 in keyword))
	{
		# printf("%4d: %s\n", NR, $0);
		e = getline;
	}
}


/^\*SPECIES/ {
	e = getline;
	j = 0;
	while ( !($0 in keyword))
	{
		if ( !(/^\*C/) )
		{
			++j;
			spe = trim($1);
			spidx[spe] = j;
			ic[j] = 0.0;
			if ( spe ~ /^[0-9].*/ )
			{
				spe = "_" spe;
			}
			gsub("-", "_", spe);
			species[j] = spe;
			# printf("%4d: %s\n", NR, $0);
		}
		e = getline;
	}
	J = j;
}


/^\*REACTION SYSTEM/ {
	e = getline;
	k = 0;
	while ( !($0 in keyword))
	{
		if ( !(/^\*C/) )
		{
			++k;
			split($0, bits, "=>");
			line = trim(bits[1]);
			reactants = sbmlnames(line, spidx, species);
			reac[k] = reactants;
			split(bits[2], morebits, "(");
			line = trim(morebits[1]);
			products = sbmlnames(line, spidx, species);
			prod[k] = products;
			split(morebits[2], rest, ")");
			rc[k] = trim(rest[1]);
			# printf("%4d: %s\n", NR, $0);
		}
		e = getline;
	}
	K = k;
}


/^\*INITIAL CONCENTRATIONS/ {
	e = getline;
	while ( !($0 in keyword) )
	{
		j = 0;
		k = split($0, bits);
		spe = trim(bits[1]);
		val = bits[k];
		if (spe in spidx) 
		{
			j = spidx[spe];
			gsub("D", "E", val);
			ic[j] = val;
			# gsub("D", "E", ic[j]);
		}
		# printf("%4d: %s\n", NR, $0);
		e = getline;
	}
}


/^\*TEMPERATURE/ {
	e = getline
	temp = -1.0;
	while ( !($0 in keyword) )
	{
		temp = $0;
		gsub("D", "E", temp);
		# printf("%4d: %s\n", NR, $0);
		e = getline;
	}
}


/^\*GAS CONSTANT/ {
	e = getline;
	gascon = -1.0;
	while ( !($0 in keyword) )
	{
		gascon = $0;
		gsub("D", "E", gascon);
		# printf("%4d: %s\n", NR, $0);
		e = getline;
	}
}


END {
	printf("%s\n", "@species"); 
	for (j = 1; j <= J; ++j)
		printf(" %s:[%s]=%E \"%s\"\n", 
                       compart[1], species[j], ic[j], species[j]);

	_RT = gascon*temp;
	XL10 = log(10.0);

	printf("%s\n", "@reactions");
	for (k = 1; k <= K; ++k)
	{
		k1 = -1.0;
		l = split(rc[k], bits, ",");
		if ( l == 1 ) { 
			k1 = bits[1];
		}
		else if ( l > 1 ) {
			# rc = ( log10(A) , E [, alpha] ) 
			# k1 = log10(A) * exp( -E / RT ) * T**(alpha)
			k1 = exp( - bits[2]/_RT + bits[1]*XL10 );
			if ( l > 2 ) k1 *= temp**bits[3];
		}
		printf("@r=%s%d \"%s%d\"\n", "reaction", k, "reaction", k);
		printf(" %s -> %s\n", reac[k], prod[k]);
		j = gsub("+", "*", reac[k]);
		if ( j > -1 ) {
			printf(" %s%d * %s : %s%d=%e\n", 
			       "p", k, reac[k], "p", k, k1);
		}
		else {
			printf(" %s%d : %s%d=%e\n", "p", k, "p", k, k1);
		}
	}
	
	printf("\n");
}


function sbmlnames(s, map, names)
{
	split(s, w, " ");
	for (kk in w)
	{
		word = trim(w[kk]);
		if (word in map)
		{
			jj = map[word];
			sub(word, names[jj], s);
		}
	}
	# printf("\nsbmlnames rtn: %s\n", s);
	return s;
}

function ltrim(s)
{
	sub(/^[ \t]+/, "", s);
	return s;
}
function rtrim(s)
{
	sub(/[ \t]+$/, "", s);
	return s;
}
function trim(s)
{
	return rtrim(ltrim(s));
}
