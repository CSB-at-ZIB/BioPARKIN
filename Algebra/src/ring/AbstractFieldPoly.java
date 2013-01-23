package ring;

import java.util.Comparator;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

import field.Field;
/**
 * The abstract polynomial field class - simply implements
 * the {@link PID#gcd(PID)} and the {@link Ring#isCommutative()}
 * methods
 * @author bzfmuell
 *
 * @param <A>
 * @param <F>
 */
public abstract class AbstractFieldPoly<A extends AbstractFieldPoly<A,F>, F extends Field<F>>
		extends MonoPoly<IntRing, F> implements PID<A> {
	public AbstractFieldPoly (){super();}
	protected AbstractFieldPoly (Comparator<IntRing> comp){super(comp);}
	public AbstractFieldPoly (IntRing index, F coeff){super(index,coeff);}
	protected AbstractFieldPoly (IntRing index, F coeff, Comparator<IntRing> comp){super(index,coeff,comp);}
	public AbstractFieldPoly(Map<IntRing,F> map){super(map);}
	protected AbstractFieldPoly (Map<IntRing,F> map, Comparator<IntRing> comp){super(map,comp);}
	public AbstractFieldPoly (MonoPoly<IntRing,F> poly) {super(poly);}
	protected AbstractFieldPoly(MonoPoly<IntRing,F> poly, Comparator<IntRing> comp){super(poly,comp);}
	public A gcd (A another){
		IntRing deg1 = getDegree(), deg2 = another.getDegree();
		@SuppressWarnings("unchecked")
		A cp  = (A) this;
		if(deg1.compareTo(deg2)<=0) {
			A mod = another.mod(cp);
			if(mod.isZero()) return cp;
			if(mod.getDegree().equals(IntRing.ZERO)) return cp;
			return cp.gcd(mod);
		}
		return another.gcd(cp);
	}
	@Override
	public boolean isCommutative (){return true;}
	public String toString (){
		StringBuilder sb = new StringBuilder ();
		Iterator<Entry<IntRing,F>> it = iterator();
		String formatStr = "%1$s X^%2$s", pls = " + ";
		while (it.hasNext()) {
			Entry<IntRing,F> entry = it.next();
			IntRing index = entry.getKey();
			if(index.compareTo(IntRing.ONE)>0) sb.append(String.format(formatStr,entry.getValue().toString(),index.toString()));
			if(index.compareTo(IntRing.ONE)==0) sb.append(String.format(formatStr,entry.getValue().toString(),index.toString()));
			if(index.compareTo(IntRing.ONE)<0) sb.append(entry.getValue().toString());
			if(it.hasNext()) sb.append(pls);
		}
		return sb.toString();
	}
}
