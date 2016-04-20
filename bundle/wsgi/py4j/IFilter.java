/*
 * Created on 21-lug-2005
 *
 * To change the template for this generated file go to
 * Window&gt;Preferences&gt;Java&gt;Code Generation&gt;Code and Comments
 */
package py4j;

import java.util.ArrayList;

public interface IFilter {
	public Double nextValue(ArrayList<Double> valueSet);//, double costante);
	public IFilter genFilter();
}
