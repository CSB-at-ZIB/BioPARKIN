package field;

import ring.CyclicRing;

public final class ThreeCycle extends AbstractField<ThreeCycle> {
	/*----------------constant fields--------------------*/
	public static final ThreeCycle ZERO = new ThreeCycle (0);
	public static final ThreeCycle  ONE = new ThreeCycle (1);
	public static final ThreeCycle  TWO = new ThreeCycle (2);
	private CyclicRing value;
	private ThreeCycle (int value){
		super();
		this.value = new CyclicRing(value,3);
	}

	public ThreeCycle inverse() {
		if(isZero()) throw new IllegalArgumentException ("\nZero division not permitted");
		return equals(ONE)?ONE:TWO;
	}

	public ThreeCycle addInverse() {return isZero()?ZERO:equals(ONE)?TWO:ONE;}

	public boolean isZero() {return value.isZero();}

	
	public ThreeCycle multiply(ThreeCycle another) {
		if(equals(ZERO)||another.equals(ZERO)) return ZERO;
		return equals(another)?ONE:TWO;
	}

	
	public ThreeCycle add(ThreeCycle another) {
		if(equals(ZERO)&&another.equals(ONE)) return ONE;
		if(equals(ZERO)&&another.equals(TWO)) return TWO;
		if(equals(ONE)&&another.equals(ZERO)) return ONE;
		if(equals(ONE)&&another.equals(ONE)) return TWO;
		if(equals(TWO)&&another.equals(ZERO)) return TWO;
		if(equals(TWO)&&another.equals(TWO)) return ONE;
		return ZERO;
	}

	
	public boolean equals(ThreeCycle another) {return value.equals(another.value)?true:false;}


	public ThreeCycle constructOne() {return ONE;}

}
