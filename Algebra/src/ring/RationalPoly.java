package ring;

import java.util.Map;
import java.util.Map.Entry;

import field.Rational;

public class RationalPoly extends AbstractFieldPoly<RationalPoly,Rational>{
	public RationalPoly (){super();}
	public RationalPoly (int[] coeffArray){
		this();
		for (int i = 0; i < coeffArray.length;i++) 	setCoefficient(new IntRing(i),new Rational(coeffArray[i]));
	}
	public RationalPoly (Rational[] coeffArray){
		this();
		for (int i = 0; i < coeffArray.length;i++) 	setCoefficient(new IntRing(i),coeffArray[i]);
	}
	public RationalPoly (IntRing index, Rational coeff){super(index,coeff);}
	public RationalPoly (Map<IntRing,Rational> coeffMap){super(coeffMap);}
	public RationalPoly (MonoPoly<IntRing,Rational> poly){super(poly);}
	public RationalPoly add(MonoPoly<IntRing,Rational> another){return new RationalPoly (super.add(another));}
	public RationalPoly addInverse (){return new RationalPoly(super.addInverse());}
	/**
	 * Returns the value of this polynomial
	 * @param arg
	 * @return
	 */
	public Rational eval(Rational arg) {
		if (arg==null) return null;
		if(isZero()) return Rational.ZERO;
		if (arg.equals(Rational.ZERO)) return getCoefficient(IntRing.ZERO);
		if (arg.equals(Rational.ONE)) {
			Rational sum = Rational.ZERO;
			for (Entry<IntRing,Rational> coeffEnt:this)sum = sum.add(coeffEnt.getValue());
			return sum;
		}
		if (arg.equals(Rational.M_ONE)) {
			Rational sum = Rational.ZERO;
			for (Entry<IntRing,Rational> coeffEnt:this){
				if(coeffEnt.getKey().mod(new IntRing(2)).equals(IntRing.ZERO)) sum = sum.add(coeffEnt.getValue());
				else sum = sum.add(coeffEnt.getValue().addInverse());
			}
			return sum;
		}
		if(IntRing.ZERO.compareTo(IntRing.ONE)<0) IntRing.reverseOrdering();
		Rational sum =Rational.ZERO;
		Rational arg1=Rational.ONE;
		long val = 0;
		for(Entry<IntRing,Rational> entry:this) {
			long key = entry.getKey().getValue();
			while(key<val) {arg1 = arg1.multiply(arg);++val;}
			sum = sum.add(entry.getValue().multiply(arg1));
		}
		return sum;
	}
	public RationalPoly mod (RationalPoly another){
		IntRing deg1 = getDegree(), deg2 = another.getDegree();
		if(deg1.compareTo(deg2)<0) return new RationalPoly(this);
		Rational coeff1 = getCoefficient(deg1), coeff2 = another.getCoefficient(deg2);
		RationalPoly mod = add(another.multiply(new RationalPoly(deg1.add(deg2.addInverse()),coeff1.multiply(coeff2.inverse()).addInverse())));
		if(mod.isZero()) return new RationalPoly(this);
		return mod.mod(another);
	}
	public RationalPoly multiply (MonoPoly<IntRing,Rational> another){return new RationalPoly(super.multiply(another));}
	
	public static void main(String[] args){
		RationalPoly p1 = new RationalPoly (new Rational[]{Rational.ONE,Rational.ZERO,Rational.ONE});
		RationalPoly p2 = new RationalPoly (new Rational[]{Rational.ONE,Rational.ZERO,Rational.ZERO,Rational.ONE});
		System.out.println(String.format("%1$s mod %2$s = %3$s",p1.toString(),p2.toString(),p1.mod(p2).toString()));
		System.out.println(String.format("gcd(%1$s, %2$s) = %3$s",p1.toString(),p2.toString(),p1.gcd(p2).toString()));
	}
}