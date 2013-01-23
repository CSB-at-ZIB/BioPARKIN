package ring;

import group.CompMonoid;

public class CyclicRing extends AbstractCommRing<CyclicRing> implements CompMonoid<CyclicRing>{
	private IntRing value;
	private IntRing   mod;
	/**
	 * 
	 */
	CyclicRing (){super();}
	public CyclicRing (int mod){this(new IntRing(mod));}
    public CyclicRing (IntRing mod){this();if(mod!=null) this.mod = mod;}
    public CyclicRing (IntRing value, IntRing mod){this(mod);setValue(value);}
    public CyclicRing (int value, int mod){this(mod);setValue(value);}
	public CyclicRing addInverse() {
		// TODO Auto-generated method stub
		return null;
	}

	public boolean isZero() {return value==null?true:value.isZero;}
	public IntRing getValue (){return value;}
	public IntRing getMod   (){return mod;}
	public CyclicRing multiply(CyclicRing another) {
		if(!mod.equals(another.mod)) throw new IllegalArgumentException ("\nDiffering mod operators... \nmod1 = "+
				mod+"\tmod2 = "+another.mod);
		return new CyclicRing (value.multiply(another.value),mod);
	}

	public CyclicRing add(CyclicRing another) {
		if(!mod.equals(another.mod)) throw new IllegalArgumentException ("\nDiffering mod operators... \nmod1 = "+
				mod+"\tmod2 = "+another.mod);
		return new CyclicRing (value.add(another.value),mod);
	}
	public void setValue (int value){setValue(new IntRing(value));}
	public void setValue (IntRing value){if(value!=null)this.value = value.mod(mod);}
	
	public boolean equals(CyclicRing another) {
		if(!mod.equals(another.mod)) return false;
		return value.equals(another.value)?true:false;
	}
	public int compareTo(CyclicRing arg0) {
		if(!mod.equals(arg0.mod)) throw new IllegalArgumentException ("Compare 2 only applicable to numbers of same modulo operator:\nthis mod = "+mod.toString()+"\targ0 mod = "+arg0.mod);
		long val1 = value.getValue(), val2 = arg0.value.getValue();
		return val1<val2?-1:val1>val2?1:0;
	}
	
	public String toString (){return value.toString()+" mod "+mod.toString();}
	
	
}
