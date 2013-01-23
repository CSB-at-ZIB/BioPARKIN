package group;

import ring.IntRing;
import field.Rational;

/**
 * The class of all cyclic groups of finite order
 * @author adin
 *
 */
public class CyclicGroup extends ComplexSphere {
	private static final String FORMAT_STRING = "%1$s \u03c0";
	/**the angle as a rational multiple of 2 pi*/
	private Rational value;
	/**
	 * Constructs the neutral element
	 */
	protected CyclicGroup (){this(Rational.ZERO);}
	/**
	 * Constructs the generator of a cyclic group of
	 * order <tt>order</tt>
	 * @param order the order of the group
	 */
	public CyclicGroup (int order){
		this(new Rational(1,order));
	}
	/**
	 * Constructs an element of a finite cyclic sub group
	 * of the complex unit sphere
	 * @param value
	 */
	public CyclicGroup (Rational value){
		super(value);
		IntRing num = value.getNumerator(), den = value.getDenominator();
		this.value = new Rational(num.mod(den),den);
	}
	/**
	 * Returns the sum of both cyclic elements. <b>Note</b>, that
	 * for two distinct denominators (orders of the groups), the 
	 * addition operation is only well defined in the <code>ComplexSphere</code>:
	 * <br />Consider for example 2 objects: <tt>x_1 in Z/nZ</tt> and <tt> x_2 in Z/mZ</tt> then
	 * <tt>x_1.add(x_2)</tt> is neither in </tt>Z/nZ</tt> nor in <tt>Z/mZ</tt>, if <tt>n</tt> &ne <tt>m</tt>
	 * 
	 * @param another
	 * @return
	 */
	public CyclicGroup add(CyclicGroup another){return new CyclicGroup(value.add(another.value));}
	
	public static void main (String[] args){
		Rational half = new Rational(1,7);
		CyclicGroup twoCycle = new CyclicGroup(half);
		CyclicGroup two      = twoCycle;
		boolean first = true;
		int count = 1;
		while (!twoCycle.equals(two)||first) {
			if(first) first = false;
			System.out.println(String.format("x^%1$d = %2$s",count,twoCycle.toString()));
			twoCycle = twoCycle.add(two);
			count++;
		}
	}
	public String toString (){
		if(equals(NEUTRAL)) return "0";
		return String.format(FORMAT_STRING, value.toString());
	}
}
