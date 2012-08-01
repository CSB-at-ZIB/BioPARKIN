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


# /^\*HEAD/ {
# 	e = getline;
# 	printf("%s:%s \"%s\"\n", 
# 	       "@model", "3.1.1=HEAD", trim($0));
# 	while ( !($0 in keyword))
# 	{
# 		# printf("%4d: %s\n", NR, $0);
# 		e = getline;
# 	}
# 	
# 	compart[1] = "cell";
# 	printf("%s\n", "@compartments");
# 	printf(" %s=%f\n", compart[1], 1.0);
# }


# /^\*ELEMENTS/ {
# 	e = getline;
# 	while ( !($0 in keyword))
# 	{
# 		# printf("%4d: %s\n", NR, $0);
# 		e = getline;
# 	}
# }


/^\*SPECIES/ {
	e = getline;
	j = 0;
	while ( !($0 in keyword) && (e == 1) )
	{
		if ( !(/^\*C/) )
		{
			++j;
			spe = trim($1);
			spidx[spe] = j;
			ic[j] = 0.0;
			hasdata[j] = 0;
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


# /^\*REACTION SYSTEM/ {
# 	e = getline;
# 	k = 0;
# 	while ( !($0 in keyword))
# 	{
# 		if ( !(/^\*C/) )
# 		{
# 			++k;
# 			split($0, bits, "=>");
# 			line = trim(bits[1]);
# 			reactants = sbmlnames(line, spidx, species);
# 			reac[k] = reactants;
# 			split(bits[2], morebits, "(");
# 			line = trim(morebits[1]);
# 			products = sbmlnames(line, spidx, species);
# 			prod[k] = products;
# 			split(morebits[2], rest, ")");
# 			rc[k] = trim(rest[1]);
# 			# printf("%4d: %s\n", NR, $0);
# 		}
# 		e = getline;
# 	}
# 	K = k;
# }


# /^\*INITIAL CONCENTRATIONS/ {
# 	e = getline;
# 	while ( !($0 in keyword) )
# 	{
# 		j = 0;
# 		k = split($0, bits);
# 		spe = trim(bits[1]);
# 		val = bits[k];
# 		if (spe in spidx) 
# 		{
# 			j = spidx[spe];
# 			gsub("D", "E", val);
# 			ic[j] = val;
# 			# gsub("D", "E", ic[j]);
# 		}
# 		# printf("%4d: %s\n", NR, $0);
# 		e = getline;
# 	}
# }


# /^\*TEMPERATURE/ {
# 	e = getline
# 	temp = -1.0;
# 	while ( !($0 in keyword) )
# 	{
# 		temp = $0;
# 		gsub("D", "E", temp);
# 		# printf("%4d: %s\n", NR, $0);
# 		e = getline;
# 	}
# }


# /^\*GAS CONSTANT/ {
# 	e = getline;
# 	gascon = -1.0;
# 	while ( !($0 in keyword) )
# 	{
# 		gascon = $0;
# 		gsub("D", "E", gascon);
# 		# printf("%4d: %s\n", NR, $0);
# 		e = getline;
# 	}
# }


/^\*MEASUREMENTS/ {
	e = getline;
	j = 0;
	m = 0;
	while ( !($0 in keyword) && (e == 1) )
	{
		if ( (!/^\*T/) && (!/^\*FINALT/) )
		{
			gsub("D", "E", $0);
			split($0, bits, ",");
			kj = 0;
			for (k in bits)  # please note: index k needs absolutely not be in order (!) 
			{
				s = trim(bits[k]);
				val = strtonum( s );
				if ( val < 0.0 )
				{
					# curstat = hasdata[j+k];
					# hasdata[j+k] = 0 || curstat;
					val = " ./. ";
				}
				else
				{
					hasdata[j+k] = 1;
				}
				if ( length(s) > 0 )
				{
					++kj;
					measure[m, j+k] = val;
				}
			}
			j += kj;
		}
		else
		{
			if (/^\*T/)
			{
				e = getline;
				gsub("D", "E", $0);
				++m;
				tp[m] = trim($0);
				measJ = j;
				j = 0;
			}
			else
			{
				e = getline;
				gsub("D", "E", $0);
				++m;
				tp[m] = trim($0);
				for (k = 1; k <= measJ; ++k)
				{
					measure[m, k] = " ./. ";
				}
			}
		}
 		# printf("%4d: %s\n", NR, $0);
		e = getline;
	}
	M = m;
	measJ = j;
}


END {
	printf("%s", "Timepoint [s]"); 
	for (j = 1; j <= measJ; ++j)
	{
		if ( hasdata[j] )
		{
			printf("\t%8s [a.u.]", species[j]);
		}
	}
	printf("\n");

	nmeas = 0;
	for (m = 1; m <= M; ++m)
	{
		printf("% 12.3f", tp[m]);
		for (j = 1; j <= measJ; ++j)
		{
			if ( hasdata[j] )
			{
				val = measure[m, j];
				if ( val ~ / \.\/\. / )
				{
					printf("\t%15s", val);
				}
				else
				{
					++nmeas;
					printf("\t% 15.7e", val);
				}
			}
		}
		printf("\n");
	}

	# printf("# nmeas = %d\n", nmeas);
}


function sbmlnames(s, map, names,     w, word, kk, jj)
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
