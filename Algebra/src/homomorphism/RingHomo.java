package homomorphism;


import ring.Ring;
/**
 * The ring homomorphism interface: by definition any implementing class is the set:
 * <p><tt>{f : {@link R} -> {@link S}| f </tt> is ring homomorphism <tt>}</tt></p>
 * <p>To specify, any implementing class must satisfy the following equivalences:
 * <ol>
 * <li><tt>f(x + y) = f(x) + f(y)</tt> for all <tt>x, y in R</tt></li>
 * <li><tt>f(x * y) = f(x) * f(y)</tt> for all <tt>x, y in R</tt></li>
 * </ol>
 * <p>An implementation could look like:</p>
 * <p><tt>public class SomeRingHomomorphism&ltR,S&gt implements RingHomo&ltSomeRingHomomorphism&ltR,S&gt,R,S&gt {<br />
 * ...//implementation<br />
 * }</tt><br />
 * 
 * @author bzfmuell
 *
 * @param <X> the type of the implementing class
 * @param <R> the type of the pre-image ring: intersection of all <tt>f^-1(im f)</tt>, where <tt>f in RingHomo</tt>
 * @param <S> the type of the image ring <tt>im f</tt>
 */
public interface RingHomo<X extends RingHomo<X,R,S>,R extends Ring<R>, S extends Ring<S>> extends
		GroupHomo<X,R,S>, Ring<X>{}
