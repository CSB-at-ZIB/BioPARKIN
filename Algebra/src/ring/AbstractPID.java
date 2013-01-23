package ring;
/**
 * The abstract {@link PID} class
 * @author bzfmuell
 *
 * @param <A>
 */
public abstract class AbstractPID<A extends AbstractPID<A>> extends
		AbstractCommRing<A> implements PID<A> {
	/**
	 * The default constructor
	 */
	public AbstractPID (){super();}
}
