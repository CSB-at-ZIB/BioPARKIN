package ring;

import group.AbstractAbel;
import group.CompMonoid;
import group.Klein4Group;

import java.util.Comparator;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;
/**
 * Polynomial class over some ring of type <{@link R}> with variables represented by some
 * monoid of type <{@link M}>. <b>Note</b>, that in fact, the monoid class used herein has
 * to implement the {@link Comparable} interface as the generic type is bounded by
 * {@link CompMonoid}. Due to that, the method {@link MonoPoly#getDegree()} strongly depends
 * on the implementation of {@link CompMonoid#compareTo(Object)} method.
 * <p><b>Note</b>, that simultaneous addition/removal of a coefficient while an iterator is
 * still moving through the coefficient map will result in an <code>ConcurrentModificationException</code>.
 * Additionally, each instance of this class is mutable - to specify there are methods able
 * to add or remove coefficients. In order to get an immutable instance, simply subclass this class
 * and override the two modifying methods {@link MonoPoly#removeCoefficient(CompMonoid)}, {@link MonoPoly#setCoefficient(CompMonoid, Ring)}
 * as:
 * <p><tt>public void setCoefficient(M index, R coeff){}</tt>, as this will leave any instance of the subclass unaltered. However,
 * the constructors must then use the super class's methods
 * @author bzfmuell
 *
 * @param <M> the type of the <code>CompMonoid</code> implementing class
 * @param <R> the type of the <code>Ring</code> implementing class
 */
public class MonoPoly<M extends CompMonoid<M>,R extends Ring<R>> extends AbstractAbel<MonoPoly<M,R>> implements
		Ring<MonoPoly<M,R>> , Iterable<Entry<M,R>>{
	/**the coefficient map: each element of the monoid is either mapped on
	 * some non-zero element or is simply not present (note null and zero are
	 * somewhat synonymous*/
	private TreeMap<M,R> coeffMap;
	/**
	 * Constructs the zero polynomial
	 */
	public MonoPoly (){super();coeffMap = new TreeMap<M,R> ();}
	/**
	 * Constructs the zero polynomial, but specifying a <code>Comparator</code>
	 * object. This may help if the ordering shall be reversed
	 * @param comp the comparator
	 */
	protected MonoPoly (Comparator<M> comp){super(); coeffMap = new TreeMap<M,R> (comp);}
	/**
	 * Constructs the monomial <tt>coeff_index * X_index</tt>
	 * @param index the monoidal index
	 * @param coeff the coefficient
	 */
	public MonoPoly (M index, R coeff){
		this();
		setCoefficient(index,coeff);
	}
	/**
	 * Constructs the monomial <tt>coeff_index * X_index</tt> but specifying
	 * a Comparator
	 * @param index the monoidal index
	 * @param coeff the coefficient
	 * @param comp the comparator
	 */
	protected MonoPoly (M index, R coeff, Comparator<M> comp){
		this(comp);
		setCoefficient(index,coeff);
	}
	/**
	 * Constructs the polynomial <tt>...+coeff_index_i * X_index_i+...</tt>,
	 * where <tt>index_i</tt> is some key and <tt>coeff_index_i</tt> is some value
	 * of the argument <tt>coeffMap</tt>
	 * @param coeffMap the coefficient map
	 */
	public MonoPoly (Map<M, R> coeffMap){
		this();
		for (Entry<M,R>entry:coeffMap.entrySet()) setCoefficient(entry.getKey(),entry.getValue()); 
	}
	/**
	 * Constructs the polynomial <tt>...+coeff_index_i * X_index_i+...</tt>,
	 * where <tt>index_i</tt> is some key and <tt>coeff_index_i</tt> is some value
	 * of the argument <tt>coeffMap</tt>. <b>Note</b>, that the parameter <tt>comp</tt>
	 * specifies a comparator.
	 * @param coeffMap the coefficient map
	 * @param comp the comparator
	 */
	protected MonoPoly (Map<M, R> coeffMap, Comparator<M> comp){
		this(comp);
		for (Entry<M,R>entry:coeffMap.entrySet()) setCoefficient(entry.getKey(),entry.getValue()); 
	}
	/**
	 * Constructs a copy of <tt>another</tt> instance of
	 * this class
	 * @param another some other instance of this class
	 */
	public MonoPoly (MonoPoly<M,R> another){this(another.coeffMap);}
	protected MonoPoly (MonoPoly<M,R> another, Comparator<M> comp){this(another.coeffMap,comp);}
	/**
	 * Returns the sum <tt>this + another</tt>
	 * @param another some other polynomial
	 * @return the sum
	 */
	public MonoPoly<M,R> add (MonoPoly<M,R> another){
		MonoPoly<M,R> sum = new MonoPoly<M,R> ();
		for (Entry<M,R> entry:this) sum.setCoefficient(entry.getKey(),entry.getValue());
		for (Entry<M,R> entry:another){
			M index = entry.getKey();
			R coeff;
			if(( coeff = sum.getCoefficient(index))!=null){
				coeff = coeff.add(entry.getValue());
				if(!coeff.isZero()) sum.setCoefficient(index, coeff);
				else sum.removeCoefficient(index);
			} else sum.setCoefficient(index, entry.getValue());
		}
		return sum;
	}
	public MonoPoly<M,R> addInverse (){
		MonoPoly<M,R> addInv = new MonoPoly<M,R> ();
		for (Entry<M,R> entry:this) addInv.setCoefficient(entry.getKey(), entry.getValue().addInverse());
		return addInv;
	}
	@SuppressWarnings("unchecked")
	public boolean equals (Object o){
		if(o == this) return true;
		if(!(o instanceof MonoPoly)) return false;
		MonoPoly<M,R> cp = (MonoPoly<M,R>) o;
		return coeffMap.equals(cp.coeffMap)?true:false;
	}
	public boolean equals (MonoPoly<M,R> another){return coeffMap.equals(another.coeffMap)?true:false;}
	/**
	 * Returns the coefficient associated with the <tt>index</tt> or
	 * null if no such coefficient exists
	 * @param index
	 * @return the coefficient or null
	 */
	public R getCoefficient (M index){R coeff = null;return (coeff = coeffMap.get(index))==null?null:coeff;}
	/**
	 * Returns the degree of this polynomial or null if
	 * this equals the zero polynomial. <b>Note</b>, that
	 * the degree depends on the <code>compareTo(CompMonoid)</code> method
	 * @return
	 */
	public M getDegree (){return coeffMap.size()==0?null:coeffMap.lastKey();}
	public int hashCode (){
		int hash = 0;
		for (Entry<M,R> entry:this) {hash += 17*entry.getKey().hashCode();hash += 37*entry.getValue().hashCode();}
		return hash;
	}
	public boolean isCommutative (){
		if(coeffMap.size()==0) return true;
		R lastCoeff = coeffMap.lastEntry().getValue();
		return lastCoeff.isCommutative()?true:false;
	}
	public boolean isZero (){return coeffMap.size()==0?true:false;}
	public Iterator<Entry<M,R>> iterator (){return coeffMap.entrySet().iterator();}
	public MonoPoly<M,R> multiply (MonoPoly<M,R> another){
		MonoPoly<M,R> prod = new MonoPoly<M,R> ();
		for (Entry<M,R> entry1:this){
			M index1 = entry1.getKey();
			R coeff1 = entry1.getValue();
			for (Entry<M,R> entry2:another) {
				M index2 = entry2.getKey();
				R coeff2 = entry2.getValue();
				R nCoeff = coeff1.multiply(coeff2); 
				M nIndex = index1.operate(index2);
				R coeff;
				if((coeff = prod.getCoefficient(nIndex))!=null) {
					coeff = coeff.add(nCoeff);
					if(!coeff.isZero()) prod.setCoefficient(nIndex, coeff);
					else prod.removeCoefficient(nIndex);
				} else prod.setCoefficient(nIndex, nCoeff);
			}
		}
		return prod;
	}
	/**
	 * Removes the <tt>index</tt> and its associated coefficient
	 * from this polynomial
	 * @param index
	 */
	public void removeCoefficient (M index){
		if(index!=null) coeffMap.remove(index);
	}
	/**
	 * Sets the coefficient to value <tt>coeff</tt> associated with
	 * the <tt>index</tt>. <b>Note</b>, that null arguments do not
	 * effect this object (no changes done)
	 * @param index the monoidal index
	 * @param coeff
	 */
	public void setCoefficient (M index, R coeff){
		if(index==null||coeff==null) return;
		if(!coeff.isZero()) coeffMap.put(index, coeff);
	}
	public String toString (){
		if(isZero()) return "0";
		StringBuilder sb = new StringBuilder ();
		String comm = " + ";
		Iterator<Entry<M,R>> it = iterator();
		while (it.hasNext()) {
			Entry<M,R> entry = it.next();
			sb.append(entry.getValue().toString());
			sb.append(entry.getKey().toString());
			if(it.hasNext()) sb.append(comm);
		}
		return sb.toString();
	}
	public static void main (String[] args){
		MonoPoly<Klein4Group,IntRing> poly1 = new MonoPoly<Klein4Group,IntRing> ();
		MonoPoly<Klein4Group,IntRing> poly2 = new MonoPoly<Klein4Group,IntRing> ();
		IntRing one  = new IntRing (1);
		IntRing mOne = new IntRing(-1);
		poly1.setCoefficient(Klein4Group.E, one);
		poly1.setCoefficient(Klein4Group.A, mOne);
		poly1.setCoefficient(Klein4Group.B, mOne);
		poly1.setCoefficient(Klein4Group.C, one);
		poly2.setCoefficient(Klein4Group.E, one);
		poly2.setCoefficient(Klein4Group.A, one);
		poly2.setCoefficient(Klein4Group.B, one);
		poly2.setCoefficient(Klein4Group.C, one);
		System.out.println(String.format("%1$s + %2$s \n= %3$s",poly1.toString(),poly2.toString(),poly1.add(poly2).toString()));
		System.out.println(String.format("(%1$s) * (%2$s) \n= %3$s",poly1.toString(),poly2.toString(),poly1.multiply(poly2).toString()));
		
	}
}
