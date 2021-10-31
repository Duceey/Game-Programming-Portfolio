using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Enemy : MonoBehaviour
{
    [Header("Health")]
    [SerializeField] private int maxHealth;

    [SerializeField] private float deathAnimationTime;

    public EnemyHealthBar enemyHealthBar;
    public int currentHealth { get; private set; }
    private Animator anim;
    private bool dead;
    private BoxCollider2D boxCollider;

    private void Awake()
    {
        currentHealth = maxHealth;
        enemyHealthBar.SetMaxHealth(maxHealth);
        anim = GetComponent<Animator>();
        boxCollider = GetComponent<BoxCollider2D>();
    }

    public void TakeDamage(int damage)
    {
        currentHealth = Mathf.Clamp(currentHealth - damage, 0, maxHealth);
        enemyHealthBar.SetHealth(currentHealth);

        if (currentHealth > 0)
            anim.SetTrigger("hurt");
        else
            Die();
    }

    private void Die()
    {
        if (!dead)
        {
            anim.SetTrigger("die");
            dead = true;
            enemyHealthBar.gameObject.SetActive(false);
            StartCoroutine(Deactivate());
        }
    }

    IEnumerator Deactivate()
    {
        yield return new WaitForSeconds(deathAnimationTime);

        gameObject.SetActive(false);
    }

    public bool Alive()
    {
        return !dead;
    }
}
