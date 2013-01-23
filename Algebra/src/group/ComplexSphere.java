package group;

import field.Rational;


/**
 * The complex unit sphere class: the set of all complex numbers
 * with modulus one
 * @author adin
 *
 */
public class ComplexSphere extends AbstractAbel<ComplexSphere> {
	/**
	 * The neutral element of the complex unit sphere (equals 1)
	 */
	public static final CyclicGroup       NEUTRAL = new CyclicGroup();
	/**
	 * The element of order two in the complex unit sphere (equals -1)
	 */
	public static final CyclicGroup          HALF = new CyclicGroup(2);
	/**The element of order four (equals the imaginary unit i)*/
	public static final CyclicGroup       QUARTER = new CyclicGroup(4);
	/**The second element of order four (equals -i)*/
	public static final CyclicGroup THREE_QUARTER = QUARTER.add(HALF);
	/**the format string*/
	private static final String FORMAT_STRING = "%1$6g \u03c0";
	/**the double precision angle in the unit interval <tt>[0,1)</tt>*/
	private double phi;
	/**
	 * Default constructor: constructs the neutral element
	 */
	protected ComplexSphere(){super();}
	/**
	 * Constructs a <code>ComplexSphere</code> object
	 * with an angle set to rational multiple of 2 pi
	 * @param phi the rational angle
	 */
	public ComplexSphere (Rational phi){this(phi.getValue());}
	/**
	 * Constructs a <code>ComplexSphere</code> object
	 * with angle <tt>phi</tt>
	 * @param phi
	 */
	public ComplexSphere (double phi){
		this();
		if(phi>=0&&1>phi) this.phi = phi;
		if(phi>=1) this.phi = phi-Math.floor(phi);
		if(phi>-1&&0>phi) this.phi = 1+phi;
		if(-1>=phi) this.phi = 1+phi-Math.floor(phi);
	}
	
	public ComplexSphere add(ComplexSphere another) {
		boolean thisIsNeutr = equals(NEUTRAL), anotherIsNeutr = another.equals(NEUTRAL);
		if(thisIsNeutr||anotherIsNeutr) return thisIsNeutr&&anotherIsNeutr?NEUTRAL:thisIsNeutr?another:this;
		return new ComplexSphere(phi+another.phi);
	}

	
	public boolean equals(ComplexSphere another) {
		if(this==another) return true;
		return Math.abs(phi-another.phi)<1e-16?true:false;
	}
	/**
	 * Returns the angle on the unit interval <tt>[0,1)</tt>
	 * @return
	 */
	public double getPhi (){return phi;}
	public String toString (){
		if(equals(NEUTRAL)) return "0";
		if(Math.abs(phi-.5)<1e-16) return "\u03c0";
		if(Math.abs(phi-.25)<1e-16) return "\u03c0/2";
		if(Math.abs(phi-.75)<1e-16) return "3/2\u03c0";
		return String.format(FORMAT_STRING,phi);
	}
}
