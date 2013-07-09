%
%  [retval] = sample_bioparkin_data( fname, tpoints, [nlevel] )
%
%  input:
%  ------
%            fname     -  a BioPARKIN data file
%            tpoints   -  new time point vector at which the 
%                          given data is resampled 
%            nlevel    -  optional: the additive noiselevel
%                          (default value: 0.01) 
%
%  output:
%  -------
%            retval    - the new data matrix WITHOUT the header line
%                        of the input fileparts
%
%  Additionally, a new file with the file name [fname '_pert' ext]
%  will be created, storing the reaampled data (but WITHOUT the SD 
%  columns, up to now ...)
% 

% Copyright (C) 2011
% Zuse Institute Berlin, Germany
% 
% Date       24/11/2011
% Written by Thomas Dierkes
%
function [retval] = sample_bioparkin_data( fname, tpoints, noise )
	
	if nargin < 2
		error('nargin too small: Missing new timepoints?') ;
		return ;
	end 
	if nargin < 3
		noise = 0.01 ;
	end

	fidin = fopen( fname ) ;
	
	if fidin < 0
		error('fopen: fidin = %d', fidin) ;
		return ;
	end
	
	
	header = fgetl(fidin) ;  % read WTHOUT trailing newline
	
	A = [] ;
	
	while ~ feof(fidin)
		line = fgets(fidin) ;
		
		a = sscanf( line, '%f') ;
		A = [ A; a'] ;
	end
	
	fclose( fidin ) ;
	
	[m,n] = size(A) ;
	
	t = A(:,1) ;
	tpoints = tpoints(:) ;
	m = length(tpoints) ;
	
	retval = [ tpoints, ...
	           interp1( t, A(:,2:n), tpoints ) + noise*randn(m,n-1) ] ;
	
	%

	[p,fn,ext] = fileparts( fname ) ;
	% fullfile(p, [fn '_pert' ext])
	fidout = fopen( fullfile(p, [fn '_pert' ext]), "w" ) ;
	
	if fidout < 0,
		error('fopen: fidout = %d', fidout) ;
		return ;
	end
	
	fprintf( fidout, '%s\n', header ) ;
	for j=1:m
		fprintf( fidout, '%g \t', retval(j,:) ) ;
		fprintf( fidout, '\n' ) ;
	end
	
	fclose( fidout ) ;
	
	
	
	
	
	
