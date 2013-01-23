package util;
import java.util.Map.Entry;
/**
 * The tuple interface: any subclass of <code>Object</code> may
 * be used as generic type
 * @author adin
 *
 * @param <X>
 */
public interface Tupleable<X> extends Iterable<Entry<Integer,X>> {
	/**
	 * Removes all entries from this <code>Tupleable</code> object
	 */
	public void clear();
	/**
	 * Returns the value associated with the argument <tt>index</tt>
	 * or null if no such index exists
	 * @param index
	 * @return
	 */
	public X getValue (int index);
	/**
	 * Returns the index associated with the argument <tt>val</tt>
	 * or null if no such value exists
	 * @param val
	 * @return
	 */
	public Integer getIndex (X val);
	public X remove (int index);
	/**
	 * Sets the entry specified by the index and value
	 * @param index
	 * @param value
	 */
	public void setEntry (int index, X value);
}
