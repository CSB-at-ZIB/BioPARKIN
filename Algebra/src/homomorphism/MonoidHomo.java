package homomorphism;

import group.Monoid;
import util.Function;
/**
 * The monoid homomorphism interface: <p>Let <tt>M</tt>, <tt>M'</tt> be two monoids and
 * <tt>X = Hom(M,M')</tt> the set of all monoid homomorphisms. Then, for two elements
 * <tt>f, g in X</tt> and some <tt>m in M</tt>, it follows:
 * <p><tt>(f * g)(m) := f(m)g(m)</tt> (to specify: component wise operation) defines a monoid
 * structure on <tt>X</tt>. The neutral element is the trivial monoid homomorphism <tt>e : M -> M'</tt>, s.t.
 * <tt>e(m) = e' in M'</tt> for all <tt>m in M</tt>
 * @author bzfmuell
 *
 * @param <M> the argument monoid type
 * @param <N> the image monoid type
 */
public interface MonoidHomo<X extends MonoidHomo<X,M,N>,M extends Monoid<M>,N extends Monoid<N>> extends Function<M,N> {
	/**
	 * Sets the current argument
	 * @param arg the argument
	 */
	public void setArgument (M arg);
	
}
