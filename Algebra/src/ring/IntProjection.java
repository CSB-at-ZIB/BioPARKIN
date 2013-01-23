package ring;

import homomorphism.GenericRingHomo;

/**
 * The projection homomorphism class <tt>p_n : Z -> Z/nZ</tt>, where <tt>n</tt> is the characteristic of the image
 * ring. <b>Note</b>, however, each of this homomorphism is unique
 * @author bzfmuell
 *
 */
public final class IntProjection extends GenericRingHomo<IntRing, CyclicRing> {
	/**the characteristic of the ring - to specify: the positive integer value <tt>n</tt>
	 * such that <tt>n * x = 0</tt> for all <tt>x in CyclicRing</tt>*/
	private IntRing characteristic;
	/**
	 * The only constructor - private to 
	 * @param characteristic
	 */
	private IntProjection (int characteristic){
		super();
		this.characteristic = new IntRing (characteristic);
	}
	
	public boolean equals(GenericRingHomo<IntRing, CyclicRing> another) {
		if(this==another) return true;
		if((this==null&&another!=null)||(this!=null&&another==null)) return false;
		CyclicRing val = another.getValue();
		return val==null?false:characteristic.getValue()==val.getMod().getValue()?true:false;
	}

	public void f() {if(arg!=null) val = new CyclicRing (arg,characteristic);else throw new RuntimeException ("\nNo argument value set...");}
	public boolean isCommutative (){return true;}
	public boolean isZero() {return characteristic.getValue()==1?true:false;}
	/**
	 * Generates the projection specified be the parameter value <tt>characteristic</tt>.
	 * <b>Note</b>:<br />
	 * <ol><li>if <tt>characteristic==0</tt> returns true, the resulting homomorphism is the identity</li>
	 * <li>if <tt>characteristic==+-1</tt> returns true, the resulting homomorphism is the zero map</li>
	 * <li>otherwise - the resulting map is simply the projection as described above</li></ol>
	 * @param characteristic the ring characteristic
	 * @return the projection homomorphism
	 */
	public static IntProjection generateProjection (int characteristic){return characteristic>=0?new IntProjection (characteristic):new IntProjection (-characteristic);}
	public static void main (String[] args){
		int modNumber = 51;
		//IntProjection p2 = generateProjection (2);
		IntProjection p3 = generateProjection (modNumber);
		String s = "f_3(%1$s) = %2$s";
		for (int i = 0; i < modNumber; i++){
			IntRing arg1 = new IntRing (i);
			for (int j = i; j < modNumber; j++){
				IntRing arg2 = new IntRing (j);
				//p2.f(arg1);
				p3.f(arg1);
				CyclicRing im1 = p3.val;
				System.out.print(String.format(s,arg1.toString(),p3.val.toString()));
				p3.f(arg1.multiply(arg2));
				CyclicRing prodIm = p3.getValue();
				p3.f(arg2);
				CyclicRing    im2 = p3.val; 
				if(prodIm.equals(im1.multiply(im2))) System.out.println(String.format("\tp3 is ring homo: f_3(%1$s * %2$s) = f_3(%1$s) * f_3(%2$s) = %3$s",arg1.toString(),arg2.toString(),prodIm.toString()));
				else System.err.println("\tp3 is not a ring homo");
			}
		}
	}
}
