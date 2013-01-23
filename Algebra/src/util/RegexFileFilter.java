/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package util;
import java.io.File;
import java.io.FileFilter;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
/**
 * A FileFilter to be used in File.listFiles(FileFilter)
 * The regex must match the whole file name (without the path)
 *
 * Example usage:
 *
 *<code>
 * File dir = new File("/my/dir");
 * File[] files = dir.listFiles(new RegexFileFilter("^\\d\\w\\w\\w.*")); //matches files starting with a pdb code
 *</code>
 *
 * @author duarte
 *
 */
public class RegexFileFilter implements FileFilter {

	private Pattern p;

	public RegexFileFilter(String regex) {
		this.p = Pattern.compile(regex);
	}

	public boolean accept(File pathname) {
		Matcher m = this.p.matcher(pathname.getName());
		if (m.matches()) return true;
		return false;
	}

}
