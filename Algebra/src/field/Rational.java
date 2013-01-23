package field;

import ring.IntRing;

/**
 * The class of all rational numbers: <tt>x = p/q</tt>, where
 * <tt>p</tt> is some integer and <tt>q</tt> some positive integer
 * such that <tt>1 = gcd(p,q)</tt> - to specify: being coprime.
 * @author adin
 *
 */
public class Rational extends AbstractField<Rational> {
	/**the numerator*/
	private IntRing   numerator;
	/**the denominator*/
	private IntRing denominator;
	/**the zero constant*/
	public static final Rational ZERO = new Rational (0);
	/**the one constant*/
	public static final Rational  ONE = new Rational (1);
	/**the minus one constant*/
	public static final Rational M_ONE= new Rational (-1);
	/**
	 * Constructs the rational number <tt>numerator/denominator</tt>, where
	 * <tt>denominator</tt> equals one
	 * @param numerator
	 * @throws IllegalArgumentException if <code>denominator==0</code> returns true
	 */
	public Rational (int numerator) throws IllegalArgumentException {this(new IntRing(numerator),IntRing.ONE);}
	/**
	 * Constructs the rational number <tt>numerator/denominator</tt>, where <tt>denominator</tt>
	 * equals one
	 * @param numerator
	 * @param denominator
	 * @throws IllegalArgumentException if <code>denominator==0</code> returns true
	 */
	public Rational (long numerator) throws IllegalArgumentException {this(new IntRing(numerator),IntRing.ONE);}
	/**
	 * Constructs the rational number <tt>numerator/denominator</tt>
	 * @param numerator
	 * @param denominator
	 * @throws IllegalArgumentException if <code>denominator==0</code> returns true
	 */
	public Rational (long numerator, long denominator) throws IllegalArgumentException {
		this(new IntRing(numerator),new IntRing(denominator));
	}

	/**
	 * Constructs the rational number <tt>numerator/denominator</tt>
	 * @param numerator
	 * @param denominator
	 * @throws IllegalArgumentException if <code>denominator==0</code> returns true
	 */
	public Rational (int numerator, int denominator) throws IllegalArgumentException {
		this(new IntRing(numerator),new IntRing(denominator));
	}
	/**
	 * Constructs the rational number <tt>numerator/denominator</tt>
	 * @param numerator
	 * @param denominator
	 * @throws IllegalArgumentException if <code>denominator.isZero()</code> returns true
	 */
	public Rational (IntRing numerator, IntRing denominator) throws IllegalArgumentException {
		super();
		int comp;
		if ((comp = denominator.compareTo(IntRing.ZERO))==0) throw new IllegalArgumentException ("\nDenominator never zero!");
		else{
			//the greatest common divisor of numerator and denominator
			IntRing gcd = numerator.gcd(denominator);
			
			//
			this.numerator   = numerator.div(gcd);
			IntRing fac = denominator.div(gcd);
			if(comp>0)this.denominator = denominator.div(gcd);
			else {this.denominator = fac.addInverse();this.numerator = numerator.addInverse();}
		}
	}
	/**
	 * Constructs a new rational number by copying the original
	 * object <tt>another</tt>
	 * @param another
	 */
	public Rational (Rational another){
		this(another.numerator,another.denominator);
	}
	public Rational add(Rational another) {
		 return new Rational (numerator.multiply(another.denominator)
		.add(denominator.multiply(another.numerator)),
		denominator.multiply(another.denominator));
	}
	
	public Rational addInverse() {return new Rational (numerator.addInverse(),denominator);}
	
	public Rational constructOne (){return ONE;}

	public boolean equals(Rational another) {return numerator.equals(another.numerator)&&denominator.equals(another.denominator)?true:false;}
	/**
	 * Returns the denominator of this rational number
	 * @return the denominator
	 */
	public IntRing getDenominator (){return denominator;}
	/**
	 * Returns the numerator of this rational number
	 * @return the numerator
	 */
	public IntRing getNumerator (){return numerator;}
	/**
	 * Returns the value of this rational number as double precision floating number
	 * @return
	 */
	public double getValue (){return ((double) numerator.getValue())/((double) denominator.getValue());}
	public Rational inverse() throws IllegalArgumentException {
		if(isZero()) throw new IllegalArgumentException ("\nZero inverse not defined...");
		return new Rational (denominator,numerator);
	}

	
	public boolean isZero() {return numerator.isZero()?true:false;}

	
	public Rational multiply(Rational another) {
		
		return another!=null?new Rational (numerator.multiply(another.numerator),
				denominator.multiply(another.denominator)):ZERO;
	}
	public String toString (){return isZero()?"0":equals(ONE)?"1":numerator.toString()+"/"+denominator.toString();}
	public static void main (String[] args){
		Rational q1 = new Rational (-2,-4);
		Rational q2 = new Rational (-1,2);
		String out = "%1$s %2$s %3$s = %4$s";
		System.out.println(String.format(out, q1,"+",q2,q1.add(q2)));
		System.out.println(String.format(out, q1,"*",q2,q1.multiply(q2)));
		System.out.println(q1.equals(q2)?String.format("%1$s equals %2$s", q1,q2):String.format("%1$s DOES NOT equal %2$s", q1,q2));
	}
	
	
}
