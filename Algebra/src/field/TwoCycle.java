package field;


public final class TwoCycle extends AbstractField<TwoCycle>{
	public static final TwoCycle ZERO = new TwoCycle ();
	public static final TwoCycle  ONE = new TwoCycle ();
	private TwoCycle (){super();}
	public TwoCycle add (TwoCycle another){
		return (equals(ZERO)&&!another.equals(ZERO))||
				(!equals(ZERO)&&another.equals(ZERO))?ONE:ZERO; 
	}
	public TwoCycle addInverse (){return equals(ZERO)?ZERO:ONE;}
	public TwoCycle constructOne (){return ONE;}
	public boolean equals (TwoCycle another) {
		if(this==another) return true;
		return false;
	}
	public TwoCycle inverse (){
		if(this==ZERO) throw new IllegalArgumentException ("Zero element not invertible...");
		return ONE;
	}
	public boolean isZero() {return equals(ZERO)?true:false;}
	public TwoCycle multiply (TwoCycle another){return equals(ZERO)||another.equals(ZERO)?ZERO:ONE;}
	public String toString (){return equals(ZERO)?"0 mod 2":"1 mod 2";}
	
	public static void main (String[] args){
		String output1 = "%1$s + %2$s = %3$s";
		String output2 = "%1$s * %2$s = %3$s";
		System.out.println(String.format(output1, ZERO,ZERO,ZERO.add(ZERO)));
		System.out.println(String.format(output1, ZERO, ONE,ZERO.add( ONE)));
		System.out.println(String.format(output1,  ONE,ZERO, ONE.add(ZERO)));
		System.out.println(String.format(output1,  ONE, ONE, ONE.add( ONE)));
		System.out.println(String.format(output2, ZERO,ZERO,ZERO.multiply(ZERO)));
		System.out.println(String.format(output2, ZERO, ONE,ZERO.multiply( ONE)));
		System.out.println(String.format(output2,  ONE,ZERO, ONE.multiply(ZERO)));
		System.out.println(String.format(output2,  ONE, ONE, ONE.multiply( ONE)));
		System.out.println(ZERO.isZero()?"is Zero":"is NOT zero");
	}
	@Override
	public boolean isCommutative() {
		// TODO Auto-generated method stub
		return false;
	}
	
	
}
