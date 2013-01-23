package homomorphism;

import java.util.HashSet;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.TreeMap;

import module.Generator;
import module.GenericVSpace;
import field.AbstractField;
import field.Rational;
import group.AbstractAbel;
import ring.Ring;
import util.ComposedObject;
/**
 * The abstract square matrices class - 
 * @author bzfmuell
 *
 * @param <F>
 */
public class AbstractMatrix<F extends AbstractField<F>> extends
		AbstractAbel<AbstractMatrix<F>> implements Ring<AbstractMatrix<F>>, VectorSHomo<AbstractMatrix<F>, GenericVSpace<F>, GenericVSpace<F>, F> {
	private TreeMap<Integer,F> coeffMap;
	private int dim;
	private GenericVSpace<F> arg;
	private GenericVSpace<F> val;
	private Generator<GenericVSpace<F>,F> generators;
	private F one;
	
	/**
	 * Constructs the zero matrix with <tt>dim</tt> rows and
	 * <tt>dim</tt> columns
	 * @param dim the dimension
	 */
	public AbstractMatrix (int dim){super();coeffMap = new TreeMap<Integer,F> (); this.dim = dim;}
	public AbstractMatrix (GenericVSpaceEndo<F> endo){
		this(endo.dim());
		generators = endo.getGenerators();
		for (ComposedObject<GenericDual<F>,GenericVSpace<F>> endoComp:endo.getEndoMap()){
			GenericDual<F> dual = endoComp.getFirst();
			GenericVSpace<F>  v = endoComp.getSecond();
			for (Entry<Integer,GenericVSpace<F>> baseElement:generators){
				Integer index = baseElement.getKey();
				GenericVSpace<F> v1 = baseElement.getValue(); 
				dual.f(v1);
				GenericDual<F> coDual = new GenericDual<F> (v1);
				coDual.f(v);
				F coeff = dual.getValue(), testCoeff = coDual.getValue();
				if(!testCoeff.isZero()) setEntry(index,coeff);
				
			}
		}
	}
	public AbstractMatrix (AbstractMatrix<F> another){
		this(another.dim);
		for (Entry<Integer,F> entry:another) if(!entry.getValue().isZero()) coeffMap.put(entry.getKey(), entry.getValue());
		if(another.arg!=null) arg = new GenericVSpace<F> (another.arg);
		if(another.generators!=null) generators = another.generators;
		if(another.one!=null) one = another.one;
	}
	/**
	 * Returns the sum <tt>this + another</tt>
	 * @param another
	 * @return
	 */
	public AbstractMatrix<F> add(AbstractMatrix<F> another) {
		if(dim!=another.dim) throw new IllegalArgumentException ("\nDimension mismatch: dim_this = "+dim+"\tdim_another = "+another.dim);
		AbstractMatrix<F> sum = new AbstractMatrix<F>(dim);
		for (Entry<Integer,F> entry:this) sum.coeffMap.put(entry.getKey(), entry.getValue());
		for (Entry<Integer,F> entry:another) {
			Integer index = entry.getKey();
			F coeff = entry.getValue(), sEntry = null;
			if((sEntry = sum.coeffMap.get(index))!=null) {
				sEntry = sEntry.add(coeff);
				if(sEntry.isZero()) sum.coeffMap.remove(index);
				else sum.coeffMap.put(index,sEntry);
			} else sum.coeffMap.put(index, coeff);
		}
		if(one!=null) sum.one = one;
		else if(another.one!=null) sum.one = another.one;
		return sum;

	}
	public AbstractMatrix<F> addInverse() {
		AbstractMatrix<F> inv = new AbstractMatrix<F> (dim);
		for (Entry<Integer,F> entry:this) inv.coeffMap.put(entry.getKey(),entry.getValue().addInverse());
		if(one!=null) inv.one = one;
		return inv;
	}
	
	public void clear() {coeffMap.clear();}
	/**
	 * Returns the determinant of this matrix
	 * @return
	 */
	public F det (){
		if(dim==2) {
			F a = getValue(0,0), b = getValue(0,1), c = getValue(1,0), d = getValue(1,1);
			if(a!=null&&b!=null&&c!=null&&d!=null) return a.multiply(d).add((b.multiply(c)).addInverse());
			if(a!=null&&d!=null) return a.multiply(d);
			if(b!=null&&c!=null) return b.multiply(c).addInverse();
			return null;
		}
		TreeMap<Integer,Integer> rowDegMap = getDegMap(true);
		int lowRow = 0, minRowDeg = Integer.MAX_VALUE;
		for (Entry<Integer,Integer> degEnt:rowDegMap.entrySet()) {
			Integer rowIndex = degEnt.getKey(), rowDeg = degEnt.getValue();
			if(rowDeg<minRowDeg) {minRowDeg = rowDeg; lowRow = rowIndex;}
		}
		TreeMap<Integer,Integer> colDegMap = getDegMap(false);
		int lowCol = 0, minColDeg = Integer.MAX_VALUE;
		for (Entry<Integer,Integer> degEnt:colDegMap.entrySet()) {
			Integer colIndex = degEnt.getKey(), colDeg = degEnt.getValue();
			if(colDeg<minColDeg) {minColDeg = colDeg; lowCol = colIndex;}
		}
		if(minRowDeg<minColDeg) {
			F det = null;
			for (int i = 0; i < dim; i++) {
				F entry;
				
				if((entry = getValue(lowRow,i))!=null) {
					if(det==null) det = ((lowRow+i)%2==0?entry:entry.addInverse()).multiply(getSubMatrix(lowRow,i).det());
					else det = (det.add((lowRow+i)%2==0?entry:entry.addInverse())).multiply(getSubMatrix(lowRow,i).det());
				}
			}
			return det;
		}
		F det = null;
		for (int i = 0; i < dim; i++) {
			F entry;
			
			if((entry = getValue(i,lowCol))!=null) {
				if(det==null) det = ((lowCol+i)%2==0?entry:entry.addInverse()).multiply(getSubMatrix(i,lowCol).det());
				else det = (det.add((lowCol+i)%2==0?entry:entry.addInverse())).multiply(getSubMatrix(i,lowCol).det());
			}
		}
		return det;
	}
	public boolean equals(AbstractMatrix<F> another) {
		if(this==another) return true;
		if(dim!=another.dim) return false;
		return add(another.addInverse()).isZero()?true:false;
	}
	public boolean equals(Object o){
		if(this==o) return true;
		if(!(o instanceof AbstractMatrix)) return false;
		if(getField().equals(((AbstractMatrix<?>) o))) {
			@SuppressWarnings("unchecked")
			AbstractMatrix<F> cp = (AbstractMatrix<F>) o;
			return equals((AbstractMatrix<F>)  cp);
		}
		return false;
	}

	public void f() {
		if(val==null) val = new GenericVSpace<F> ();
		for (Entry<Integer,F> coeff:this) {
			Integer index = coeff.getKey();
			int col = index%dim, row = (index-col)/dim;
			F vectorEntry = arg.getValue(col), valEntry = null, prod = coeff.getValue().multiply(vectorEntry);
			if((valEntry = val.getValue(row))!=null) {
				valEntry = valEntry.add(prod);
				if(!valEntry.isZero()) val.setEntry(row,valEntry);
				else val.remove(row);
			} else val.setEntry(row, prod);
		}
		
	}
	
	public void f(GenericVSpace<F> arg) {
		this.arg = arg;
		f();
	}
	public GenericVSpace<F> getArgument() {return arg==null?null:arg;}
	public Integer getIndex(F val) {
		for (Entry<Integer,F> entry:this) if(entry.getValue().equals(val)) return entry.getKey();
		return null;
	}
	/**
	 * Returns the type of the underlying field as a class object
	 * @return the field type
	 */
	public Class<?> getField(){return one.getClass();}
	/**
	 * Returns the submatrix of this matrix with rows from <tt>rowStart</tt> to <tt>rowStart + dim - 1</tt> and columns
	 * from <tt>colStart</tt> to <tt>colStart + dim - 1</tt>
	 * @param rowStart the row starting index
	 * @param colStart the column starting index
	 * @param dim the matrix dimension
	 * @return the submatrix
	 * @throws IllegalArgumentException if <ol><li>the <tt>dim</tt> argument is non-positive</li><li><tt>dim - x</tt> exceeds this matrix's dimension, where <tt>x = rowStart, colStart</tt></li></ol>
	 */
	public AbstractMatrix<F> getSubMatrix (int rowStart, int colStart, int dim) throws IllegalArgumentException {
		if(dim<=0) throw new IllegalArgumentException ("\nNon-positive dimension: "+dim);
		if(dim-rowStart>this.dim||dim-colStart>this.dim) throw new IllegalArgumentException ("\nSubmatrix's dimension exceeds this matrix's dimension!\n"+(dim-rowStart>this.dim?"row: "+rowStart:"col: "+colStart));
		AbstractMatrix<F> subMatrix = new AbstractMatrix <F> (dim);
		for (Entry<Integer,F> entry:this) {
			Integer index = entry.getKey();
			int col = index%dim, row = (index-col)/dim;
			int relrow = row-rowStart, relcol = col-colStart;
			if(0<=relrow&&relrow<dim&&0<=relcol&&relcol<dim) subMatrix.setEntry(relrow, relcol, entry.getValue());
		}
		if(one!=null) subMatrix.one = one;
		return subMatrix;
	}
	/**
	 * Returns the sub matrix of this matrix with the row <tt>rowExclude</tt> and column <tt>colExclude</tt>
	 * omitted. The submatrix is of dimension <tt>this.dim - 1</tt>
	 * @param rowExclude the row index to exclude
	 * @param colExclude the column index to exclude
	 * @return
	 * @throws IllegalArgumentException
	 */
	public AbstractMatrix<F> getSubMatrix (int rowExclude, int colExclude) throws IllegalArgumentException {
		if(rowExclude>=dim||colExclude>=dim) throw new IllegalArgumentException ("\nExclusion value exceeds matrix dimension: "+(rowExclude>=dim?"row: "+rowExclude:"col: "+colExclude));
		AbstractMatrix<F> subMatrix = new AbstractMatrix <F> (dim-1);
		for (Entry<Integer,F> entry:this) {
			Integer index = entry.getKey();
			int col = index%dim, row = (index-col)/dim;
			if(col!=colExclude&&row!=rowExclude) subMatrix.setEntry(row<rowExclude?row:row-1, col<colExclude?col:col-1, entry.getValue());
		}
		if(one!=null) subMatrix.one = one;
		return subMatrix;
	}
	public GenericVSpace<F> getValue() {
		if(val==null&&arg!=null) f();
		return val==null?null:val;
	}
	public F getValue(int index) {
		F coeff = coeffMap.get(index);
		return coeff==null?null:coeff;
	}
	
	public F getValue (int row, int col){
		return getValue(row*dim+col);
	}
	

	public boolean isCommutative() {return false;}
	
	public boolean isZero() {return coeffMap.size()==0?true:false;}
	
	

	
	public Iterator<Entry<Integer, F>> iterator() {return coeffMap.entrySet().iterator();}
	public AbstractMatrix<F> multiply(AbstractMatrix<F> another) {
		if(dim!=another.dim) throw new IllegalArgumentException ("\nMatrix dimension mismatch: this dim = "+dim+"\t another dim = "+another.dim);
		AbstractMatrix<F> prod = new AbstractMatrix<F> (dim);
		for (Entry<Integer,F> entryLeft:this){
			Integer index1 = entryLeft.getKey();
			int colL = index1%dim, rowL = (index1-colL)/dim ; 
			F coeff1       = entryLeft.getValue();
			for (Entry<Integer,F> entryRight:another) {
				Integer index2 = entryRight.getKey();
				int colR  = index2%dim, rowR = (index2-colR)/dim;
				if(rowR!=colL) continue;
				F coeff2       = entryRight.getValue(), prodEnt = null;
				Integer nIndex = rowL*dim+colR;
				F product = coeff1.multiply(coeff2);
				if((prodEnt = prod.coeffMap.get(nIndex))!=null) {
					prodEnt = prodEnt.add(product);
					if(!prodEnt.isZero()) prod.coeffMap.put(nIndex, prodEnt);
					else prod.coeffMap.remove(nIndex);
				} else prod.coeffMap.put(nIndex, product);
			}
		}
		if(one!=null) prod.one = one;
		else if(another.one!=null) prod.one = another.one;
		return prod;
	
	}
	public AbstractMatrix<F> multiply(F scalar) {
		AbstractMatrix<F> scl = new AbstractMatrix<F> (dim);
		for (Entry<Integer,F> entry:this) scl.coeffMap.put(entry.getKey(), entry.getValue().multiply(scalar));
		if(one!=null) scl.one = one;
		return scl;
	}
	public AbstractMatrix<F> ringAct(F scalar) {return multiply(scalar);}
	public F remove (int index){return coeffMap.remove(index);}
	public void setArgument(GenericVSpace<F> arg) {
		this.arg = arg;
		
	}
	/**
	 * Sets the dimension of the underlying vector space on which
	 * this matrix object acts. <b>Note</b>, the dimension will
	 * only be changed if <tt>dim>=11</tt> returns true
	 * @param dim the dimension
	 */
	public void setDim(int dim){
		if(dim>=1) this.dim = dim;
	}
	
	
	public void setEntry(int index, F value) {
		int col = index%dim;
		int row = (index - col)/dim;
		setEntry(row,col,value);
	}
	
	
	
	
	
	
	/**
	 * Sets this matrix's entry to <tt>coeff</tt> at position
	 * <tt>(row,col)</tt>
	 * @param row the row index
	 * @param col the column index
	 * @param coeff the coefficient
	 */
	public void setEntry (int row, int col, F coeff){
		if(one==null) {
			one = coeff.constructOne();
			if(generators==null||generators.rank()==0) createCanonGenerators();
		}
		if(row>=0&&row<dim&&col>=0&&col<dim){
			if(!coeff.isZero()) coeffMap.put(dim*row+col, coeff);
		}
	}
	/**
	 * Adds the sub matrix <tt>subMat</tt> to this matrix object starting
	 * at row index <tt>rowStart</tt> and column index <tt>colStart</tt>
	 * @param subMat the sub matrix
	 * @param rowStar the row starting index
	 * @param colStart the column starting index
	 * @throws IllegalAgumentException the dimension of the sub matrix either
	 * exceeds this matrix's dimension or the starting index <tt>(rowStart,colStart)</tt>
	 * violates this matrix's dimension
	 */
	public void setSubMatrix (AbstractMatrix<F> subMat, int rowStart, int colStart) throws IllegalArgumentException {
		if(subMat.dim>=dim) throw new IllegalArgumentException (String.format("\nDimension out of range: this_dim = %1$d\tsubMat_dim = %2$d",dim,subMat.dim));
		if(subMat.dim+rowStart>=dim||subMat.dim+colStart>=dim)
			throw new IllegalArgumentException ();
		for (int i = 0; i < subMat.dim; i++){
			for (int j = 0; j < subMat.dim; j++){
				F newEntry = subMat.getValue(i, j), oldEntry = getValue(i,j);
				if(newEntry!=null) setEntry(i,j,newEntry);
				else if(oldEntry!=null) remove(dim*i+j);
				
			}
		}
	}
	public String toString (){
		String com = " , ", brackOn = "[", brackOff = "]", nl = "\n";
		StringBuilder sb = new StringBuilder (brackOn);
		//F zero = null;
		for (int i = 0; i < dim; i++){
			sb.append(brackOn);
			for (int j = 0; j < dim; j++) {
				F ent = getValue(i,j);
				if(ent!=null) sb.append(ent.toString());
				else sb.append("0");
				if(j<dim-1) sb.append(com);
			}
			sb.append(brackOff);
			if(i<dim-1)sb.append(nl);
		}
		sb.append(brackOff);
		return sb.toString();
	}
	public AbstractMatrix<F> transpose (){
		AbstractMatrix<F> trans = new AbstractMatrix <F> (dim);
		for (Entry<Integer,F> entry:this) {
			Integer index = entry.getKey();
			int col = index%dim, row = (index-col)/dim;
			trans.setEntry(col, row, entry.getValue());
		}
		return trans;
	}
	private TreeMap<Integer,Integer> getDegMap (boolean rowCol){
		TreeMap<Integer,Integer> degMap = new TreeMap<Integer,Integer> ();
		for (Entry<Integer,F> entry:this) {
			Integer index = entry.getKey();
			int col = index%dim, row = (index-col)/dim;
			if(rowCol) {
				Integer deg = null;
				if((deg = degMap.get(row))!=null) degMap.put(row, deg++);
				else degMap.put(row, 1);
			} else {
				Integer deg = null;
				if((deg = degMap.get(col))!=null) degMap.put(col, deg++);
				else degMap.put(col, 1);
			}
		}
		return degMap;
	}
	/**
	 * Creates the canonical basis of the underlying vector space
	 */
	private void createCanonGenerators (){
		if(dim>0){
			HashSet<GenericVSpace<F>> genSet = new HashSet<GenericVSpace<F>> ();
			for (int i = 0; i < dim; i++) {GenericVSpace<F> v = new GenericVSpace<F> ();v.setEntry(i, one);genSet.add(v);}
			generators = new Generator<GenericVSpace<F>,F> (genSet);
		}
	}
	/**
	 * Constructs the identity matrix <tt>I_dim</tt>
	 * @param one some non zero field element
	 * @param dim the dimension
	 * @return the identity matrix
	 * @throws IllegalArgumentException if <tt>one.isZero()</tt> returns true
	 */
	public static <F extends AbstractField<F>> AbstractMatrix<F> identity(F one, int dim) throws IllegalArgumentException
	{
		if(one.isZero()) throw new IllegalArgumentException ("\nOnly non zero arguments excepted!");
		F one1 = one.constructOne();
		AbstractMatrix<F> id = new AbstractMatrix<F> (dim);
		for (int i = 0; i < dim; i++) id.setEntry(i, i, one1);
		return id;
	}
	public static void main (String[] args){
		AbstractMatrix<Rational> two = new AbstractMatrix<Rational> (3);		
		two.setEntry(0, 1, Rational.M_ONE);
		two.setEntry(0, 2, Rational.ONE.add(Rational.ONE));
		two.setEntry(1, 0, Rational.ONE);
		two.setEntry(1, 2, Rational.M_ONE);	
		two.setEntry(2, 0, Rational.ONE.add(Rational.ONE.add(Rational.ONE)));
		two.setEntry(2, 2, Rational.ONE);
		AbstractMatrix<Rational>  cp = new AbstractMatrix<Rational>(two), id = AbstractMatrix.identity(Rational.ONE, cp.dim);
		System.out.println(String.format("det \n%1$s = %2$s", two,two.det()));
		System.out.println(String.format("\n%1$s^t = \n%2$s", two,two.transpose()));
		int pow = 1;
		while (!cp.equals(id)) {
			System.out.println(String.format("x^%1$d = %2$s",pow,cp.toString()));
			cp = cp.multiply(two);
			pow += 1;
		}
		
	}
}
