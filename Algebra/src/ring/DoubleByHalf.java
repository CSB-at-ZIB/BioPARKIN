package ring;

import java.util.Comparator;
import java.util.Map;

import field.TwoCycle;

public class DoubleByHalf extends MonoPoly<IntRing,TwoCycle> {
	private static final Comparator<IntRing> LOCAL_COMP = new Comparator<IntRing> (){

		public int compare(IntRing o1, IntRing o2) {return o2.compareTo(o1);}
		
	};
	private short  sign;
	private int  cutoff;
	private double prec;
	public DoubleByHalf (float value){
		this((double) value);
	}
	public DoubleByHalf (double value){
		super(LOCAL_COMP);
		cutoff = 30;
		prec = Math.pow(.5, cutoff);
		if(value<0) sign = 1;
		setElement(value);
	}
	private void setElement (double value){
		double val;
		if(sign==0) val = value;
		else val = -value;
		int pow = (int) Math.floor(Math.log(val)/Math.log(2d));
		double two = Math.pow(2, pow);
		while (pow>=-cutoff&&val>prec) {
			val = val - two; 
			if (val<0) val = val+two;
			else setCoefficient (new IntRing (pow),TwoCycle.ONE);
			pow--;
			two = .5*two;
		}
	}
	public String toString (){
		StringBuilder sb = new StringBuilder ();
		long lastIndex = getDegree().getValue();
		boolean below0 = false;
		for (Map.Entry<IntRing, TwoCycle> coeffs:this){
			long index = coeffs.getKey().getValue();
			while (lastIndex-index>1) {sb.append("0");lastIndex--;}
			if(index<0&&!below0) {sb.append(".");below0 = true;}
			lastIndex = index;
			sb.append("1");
		}
		return sb.toString();
	}
	public static void main (String[] args){
		double x = 965898765.6223233321340;
		DoubleByHalf dh = new DoubleByHalf (x);
		System.out.println(dh.toString());
	}
}
