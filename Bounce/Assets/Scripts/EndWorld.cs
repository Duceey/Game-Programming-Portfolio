using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EndWorld : MonoBehaviour
{
    private void OnTriggerEnter2D(Collider2D collision)
    {
        WorldControl.instance.WorldComplete();
    }
}
