using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerHealth : MonoBehaviour
{
    [SerializeField] private int maxHealth = 100;
    public HealthBar healthBar;
    private int currentHealth;
    private bool dead = false;

    Animator anim;

    private void Start()
    {
        currentHealth = maxHealth;
        healthBar.SetMaxHealth(maxHealth);
        anim = GetComponent<Animator>();
    }

    public void TakeDamage(int damage)
    {
        currentHealth -= damage;

        healthBar.SetHealth(currentHealth);

        anim.SetTrigger("hurt");

        if (currentHealth <= 0 && Alive())
            Die();
    }

    private void Die()
    {
        dead = true;

        anim.SetTrigger("die");

        Debug.Log("Player died!");
    }

    public bool Alive()
    {
        return !dead;
    }
}
