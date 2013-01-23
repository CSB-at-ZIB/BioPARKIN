package field;

public class DoubleField extends AbstractField<DoubleField> implements Comparable<DoubleField>{
	public static final DoubleField ZERO = new DoubleField();
	public static final DoubleField  ONE = new DoubleField(Rational.ONE);
	public static final DoubleField M_ONE= new DoubleField(Rational.M_ONE);
	private double value;
	public DoubleField() {this(0);}
	
	public DoubleField(double value){
		super();
		this.value = value;
	}
	public DoubleField (Rational value){this(value.getValue());}

	
	public DoubleField inverse() {
		if(isZero()) throw new IllegalArgumentException("\nZero division");
		double one = 1, inv = 1/value, diff = Math.abs(value*inv-one);
		while (diff>5e-16) {
			inv += one-value*inv;
			diff = Math.abs(value*inv-one);}		
		return new DoubleField(inv);
	}

	
	public DoubleField addInverse() {return new DoubleField(-value);}

	public int compareTo(DoubleField another){
		return value<another.value?-1:value>another.value?1:0;
	}
	
	public boolean isZero() {return Math.abs(value)<1e-20?true:false;}

	
	public DoubleField multiply(DoubleField another) {return new DoubleField(value*another.value);}

	
	public DoubleField add(DoubleField another) {return new DoubleField(value+another.value);}

	
	public boolean equals(DoubleField another) {
		if(this==another) return true;
		return Math.abs(value-another.value)<5e-16?true:false;
	}

	public double getValue(){return value;}
	
	public DoubleField constructOne (){return ONE;}
		
	public String toString(){return ""+value;}
	
	public static void main(String[] args){
		DoubleField val = new DoubleField(.0000000187023405456400037223223113123205);
		System.out.println(val.inverse());
	}

}
