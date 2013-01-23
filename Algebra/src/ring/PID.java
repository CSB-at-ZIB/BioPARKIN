package ring;
/**
 * The principal ideal domain interface: the sole method to implement
 * is the {@link PID#gcd(PID)} returning the greatest common divisor of
 * two elements of the implementing class
 * @author bzfmuell
 *
 * @param <P> the type of the <code>PID</code>
 */
public interface PID<P extends PID<P>>{
	/**
	 * Returns the greatest common divisor <br /><tt>gcd(this,another)</tt>
	 * @param another another <code>PID</code> element
	 * @return the greatest common divisor
	 */
	public P gcd(P another);
	public P mod (P another);
}
